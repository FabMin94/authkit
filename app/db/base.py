from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# The engine is the connection pool to PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # logs all SQL - turn off in production 
)

# Session factory - each request gets its own session
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all models
class Base(DeclarativeBase):
    pass