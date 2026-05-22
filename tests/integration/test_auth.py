import pytest
from httpx import AsyncClient


async def test_register_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "secret123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data
    assert "id" in data


async def test_register_duplicate_email(client: AsyncClient):
    payload={"email": "test@example.com", "password": "secret123"}
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


async def test_register_invalid_email(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "thisisnotanemail",
        "password": "secret123",
    })
    assert response.status_code == 422


async def test_login_success(client: AsyncClient):
    payload={"email": "test@example.com", "password": "secret123"}
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "secret123",
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "email": "nobody@example.com",
        "password": "secret123",
    })
    assert response.status_code == 401


async def test_get_me_success(client: AsyncClient):
    payload={"email": "test@example.com", "password": "secret123"}
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=payload)
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me", 
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


async def test_get_me_no_token(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


async def test_get_me_fake_token(client: AsyncClient):
    response = await client.get(
        "/api/v1/auth/me", 
        headers={"Authorization": "Bearer this.is.not.a.token"},
    )
    assert response.status_code == 401
