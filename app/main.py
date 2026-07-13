from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="Customer Support AI",
    description="Backend API for AI-powered customer support.",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "message": "Backend Running 🚀"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }