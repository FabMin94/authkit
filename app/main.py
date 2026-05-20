from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base, engine
from app.models import user   # noqa: F401 - import so SQLAlchemy sees the model
from app.api.v1.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose engine
    await engine.dispose()


app = FastAPI(
    title="AuthKit",
    description="A standalone authentication microservice",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "authkit"}