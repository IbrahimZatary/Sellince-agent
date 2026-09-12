from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_opaque_token,
    hash_opaque_token,
    hash_password,
    verify_password,
)
from app.models.company import Company
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateMeRequest,
    UserMeResponse,
)

bearer_scheme = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["auth"])


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def set_refresh_cookie(response: JSONResponse, token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        max_age=int(settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )


def create_refresh_token_record(user_id: int) -> tuple[RefreshToken, str]:
    raw_token = generate_opaque_token()
    token_record = RefreshToken(
        user_id=user_id,
        token_hash=hash_opaque_token(raw_token),
        expires_at=utc_now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return token_record, raw_token


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppException(
            status_code=401,
            error_code="MISSING_TOKEN",
            message="Authentication token is required",
        )

    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise AppException(
            status_code=401,
            error_code="INVALID_TOKEN",
            message="Token missing subject",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise AppException(
            status_code=404,
            error_code="USER_NOT_FOUND",
            message="User not found",
        )
    return user


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise AppException(
            status_code=409,
            error_code="EMAIL_EXISTS",
            message="Email already registered",
        )

    company = Company(
        name=request.company_name,
        sector=request.sector,
        subscription_tier=request.subscription_tier,
    )
    db.add(company)
    db.flush()

    user = User(
        company_id=company.id,
        full_name=request.full_name,
        email=request.email,
        password_hash=hash_password(request.password),
        role="admin",
    )
    db.add(user)
    db.flush()

    refresh_token_record, refresh_token = create_refresh_token_record(user.id)
    db.add(refresh_token_record)
    db.commit()

    response = JSONResponse(
        content={
            "access_token": create_access_token({"sub": str(user.id)}),
            "token_type": "bearer",
        }
    )
    set_refresh_cookie(response, refresh_token)
    return response


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise AppException(
            status_code=401,
            error_code="INVALID_CREDENTIALS",
            message="Invalid email or password",
        )

    refresh_token_record, refresh_token = create_refresh_token_record(user.id)
    db.add(refresh_token_record)
    db.commit()

    response = JSONResponse(
        content={
            "access_token": create_access_token({"sub": str(user.id)}),
            "token_type": "bearer",
        }
    )
    set_refresh_cookie(response, refresh_token)
    return response


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise AppException(
            status_code=401,
            error_code="MISSING_REFRESH_TOKEN",
            message="Refresh token not found",
        )

    token_record = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == hash_opaque_token(refresh_token))
        .first()
    )
    if not token_record:
        raise AppException(
            status_code=401,
            error_code="INVALID_REFRESH_TOKEN",
            message="Refresh token is invalid",
        )

    if token_record.expires_at < utc_now():
        raise AppException(
            status_code=401,
            error_code="REFRESH_TOKEN_EXPIRED",
            message="Refresh token has expired",
        )

    if token_record.revoked_at is not None:
        raise AppException(
            status_code=401,
            error_code="REFRESH_TOKEN_REVOKED",
            message="Refresh token has been revoked",
        )

    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise AppException(
            status_code=404,
            error_code="USER_NOT_FOUND",
            message="User not found",
        )

    token_record.revoked_at = utc_now()
    new_token_record, new_refresh_token = create_refresh_token_record(user.id)
    db.add(new_token_record)
    db.commit()

    response = JSONResponse(
        content={
            "access_token": create_access_token({"sub": str(user.id)}),
            "token_type": "bearer",
        }
    )
    set_refresh_cookie(response, new_refresh_token)
    return response


@router.get("/me")
def get_current_user_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    return UserMeResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role,
        company_id=current_user.company_id,
        company_name=company.name if company else "",
        sector=company.sector if company else None,
        subscription_tier=company.subscription_tier if company else None,
    )


@router.patch("/me", response_model=UserMeResponse)
def update_current_user(
    request: UpdateMeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.id == current_user.company_id).first()

    if request.full_name is not None:
        current_user.full_name = request.full_name
    if request.company_name is not None and company is not None:
        company.name = request.company_name
    if request.sector is not None and company is not None:
        company.sector = request.sector
    if request.subscription_tier is not None and company is not None:
        company.subscription_tier = request.subscription_tier

    db.commit()
    db.refresh(current_user)
    if company is not None:
        db.refresh(company)

    return UserMeResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role,
        company_id=current_user.company_id,
        company_name=company.name if company else "",
        sector=company.sector if company else None,
        subscription_tier=company.subscription_tier if company else None,
    )


@router.post("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        token_record = (
            db.query(RefreshToken)
            .filter(RefreshToken.token_hash == hash_opaque_token(refresh_token))
            .first()
        )
        if token_record is not None and token_record.revoked_at is None:
            token_record.revoked_at = utc_now()
            db.commit()

    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
    return response
