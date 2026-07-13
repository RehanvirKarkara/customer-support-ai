from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.tickets import router as ticket_router

app = FastAPI(
    title="Customer Support AI",
    description="Backend API for AI-powered customer support.",
    version="1.0.0",
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    ticket_router,
    prefix="/api/v1"
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