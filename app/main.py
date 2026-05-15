from fastapi import FastAPI

app = FastAPI(
    title="AuthKit",
    description="A standalone authentication microservice",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "authkit"}