from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import hash_password


class UserAlreadyExistsError(Exception):
    pass


async def create_user(db: AsyncSession, data: UserRegister) -> User:
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise UserAlreadyExistsError(f"Email {data.email} is already registered")

    # Create new user
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.flush()  # sends INSERT to DB but doesn't commit yet
    await db.refresh(user)  # loads DB-generated fields (id, created_at, etc.)
    return user