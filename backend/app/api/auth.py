from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.models.company import Company
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateMeRequest,
    UserMeResponse,
)
from app.services.auth_service import (
    login_user,
    refresh_token_session,
    register_new_user,
    revoke_token,
    update_user_profile,
    utc_now,
)

bearer_scheme = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["auth"])


def set_refresh_cookie(response: JSONResponse, token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        max_age=int(settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )


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
    token_payload, refresh_token = register_new_user(db=db, request=request)
    response = JSONResponse(content=token_payload)
    set_refresh_cookie(response, refresh_token)
    return response


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    token_payload, refresh_token = login_user(db=db, request=request)
    response = JSONResponse(content=token_payload)
    set_refresh_cookie(response, refresh_token)
    return response


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    token_payload, new_refresh_token = refresh_token_session(db=db, refresh_token=refresh_token)
    response = JSONResponse(content=token_payload)
    set_refresh_cookie(response, new_refresh_token)
    return response


@router.get("/me", response_model=UserMeResponse)
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
    return update_user_profile(db=db, current_user=current_user, request=request)


@router.post("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    revoke_token(db=db, refresh_token=refresh_token)

    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
    return response
