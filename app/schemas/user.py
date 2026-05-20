from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

# --- Request schemas (what the client sends) ---

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Response schemas (what the API returns) ---

class UserResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"