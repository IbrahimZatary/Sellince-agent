from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_opaque_token,
    hash_opaque_token,
)
from jose import jwt
from app.core.config import settings


def test_hash_and_verify_password():
    plain = "MySecurePassword123"
    hashed = hash_password(plain)

    # Same password verifies
    assert verify_password(plain, hashed)

    # Different password doesn't verify
    assert not verify_password("WrongPassword", hashed)


def test_password_hash_is_different():
    """Same password hashed twice should produce different hashes (salt)"""
    plain = "SamePassword123"
    hash1 = hash_password(plain)
    hash2 = hash_password(plain)

    # Hashes should be different due to salt
    assert hash1 != hash2
    # But both should verify
    assert verify_password(plain, hash1)
    assert verify_password(plain, hash2)


def test_create_access_token():
    data = {"sub": "123"}
    token = create_access_token(data)

    # Token should decode successfully
    decoded = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_access_token_algorithm():
    """Verify token uses correct algorithm"""
    data = {"sub": "456"}
    token = create_access_token(data)

    decoded = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    # Token should have correct claims
    assert decoded["sub"] == "456"


def test_opaque_token_generation():
    token1 = generate_opaque_token()
    token2 = generate_opaque_token()

    # Tokens should be different and long
    assert token1 != token2
    assert len(token1) > 50
    assert len(token2) > 50


def test_opaque_token_deterministic():
    """Same opaque token should always hash to same value"""
    token = generate_opaque_token()
    hash1 = hash_opaque_token(token)
    hash2 = hash_opaque_token(token)

    assert hash1 == hash2


def test_opaque_token_hashing():
    token = generate_opaque_token()
    hash1 = hash_opaque_token(token)
    hash2 = hash_opaque_token(token)

    # Same token → same hash
    assert hash1 == hash2

    # Hash is 64 chars (SHA-256 hex)
    assert len(hash1) == 64


def test_opaque_token_hash_different_tokens():
    """Different tokens should produce different hashes"""
    token1 = generate_opaque_token()
    token2 = generate_opaque_token()

    hash1 = hash_opaque_token(token1)
    hash2 = hash_opaque_token(token2)

    assert hash1 != hash2
