# AuthKit

[![CI](https://github.com/FabMin94/authkit/actions/workflows/ci.yml/badge.svg)](https://github.com/FabMin94/authkit/actions/workflows/ci.yml)

A self-hostable JWT authentication microservice built with FastAPI and PostgreSQL.
Designed to be used as a standalone auth layer for other services — register users,
issue tokens, and validate them via a simple HTTP API.

---

## Architecture

```
Client
  │
  ▼
POST /api/v1/auth/register   → create user, hash password (bcrypt)
POST /api/v1/auth/login      → verify credentials, issue JWT
GET  /api/v1/auth/me         → validate token, return user profile
  │
  ▼
PostgreSQL
  └── users (id, email, hashed_password, is_active, is_superuser)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy (async) |
| Auth | JWT via python-jose, bcrypt |
| Config | pydantic-settings |
| Testing | pytest + pytest-asyncio + httpx |
| Linting | ruff |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions → GHCR |

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker + Docker Compose
- [uv](https://github.com/astral-sh/uv)

### 1. Clone and install

```bash
git clone https://github.com/FabMin94/authkit.git
cd authkit
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your `SECRET_KEY`:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start the database

```bash
docker compose up -d db
```

### 4. Run the app

```bash
uv run python main.py
```

Visit `http://localhost:8000` for the interactive demo UI,
or `http://localhost:8000/docs` for the full API documentation.

---

## API Reference

### Register

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Response `201`:
```json
{
  "id": "a1b2c3d4-...",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-01T00:00:00Z"
}
```

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Response `200`:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Get current user

```http
GET /api/v1/auth/me
Authorization: Bearer eyJhbGc...
```

Response `200`:
```json
{
  "id": "a1b2c3d4-...",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

## Running Tests

```bash
# Start the database
docker compose up -d db

# Run all tests
uv run pytest -v

# Unit tests only
uv run pytest tests/unit -v

# Integration tests only
uv run pytest tests/integration -v
```

---

## Using AuthKit in Another Service

AuthKit is designed to be used as an auth layer for other services.
To validate a token from another service, call `/api/v1/auth/me`:

```python
import httpx

async def verify_token(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://your-authkit-url/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
    if response.status_code != 200:
        raise ValueError("Invalid token")
    return response.json()
```

See [PriceRadar](https://github.com/FabMin94/priceradar) for a real-world example.

---

## Project Structure

```
authkit/
├── app/
│   ├── api/v1/        # Route handlers
│   ├── core/          # Config, security utilities
│   ├── db/            # Database connection, session
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic request/response schemas
│   └── services/      # Business logic
├── static/            # Demo frontend
├── tests/
│   ├── unit/          # Pure function tests
│   └── integration/   # Full API flow tests
├── docker-compose.yml
├── Dockerfile
└── main.py
```