from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base, engine
from app.models import user   # noqa: F401 - import so SQLAlchemy sees the model

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

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "authkit"}