from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

from app.routes.ai import router as ai_router
from app.routes.opportunities import router as opportunities_router
from app.routes.profile import router as profile_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="PrepPath AI - Opportunity-to-Application Readiness Platform API",
    version="0.1.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(ai_router)
app.include_router(opportunities_router)
app.include_router(profile_router)


@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }


@app.get("/")
def root():
    """Root endpoint presenting API overview."""
    return {
        "message": "Welcome to PrepPath AI API",
        "docs": "/docs",
        "health": "/health"
    }
