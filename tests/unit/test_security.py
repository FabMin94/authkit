from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_different_string():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"


def test_hash_password_is_not_deterministic():
    """Same password should produce different hashes (bcrypt uses random salt)."""
    hash1 = hash_password("mypassword")
    hash2 = hash_password("mypassword")
    assert hash1 != hash2


def test_verify_password_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token_returns_string():
    token = create_access_token("test@example.com")
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token_returns_subject():
    token = create_access_token("test@example.com")
    sub = decode_access_token(token)
    assert sub == "test@example.com"


def test_decode_access_token_invalid_token():
    result = decode_access_token("this.is.not.a.valid.token")
    assert result is None


def test_decode_access_token_tampered_token():
    token = create_access_token("test@example.com")
    tampered = token + "tampered"
    result = decode_access_token(tampered)
    assert result is None
