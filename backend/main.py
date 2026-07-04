""""
CivicMind AI - FastAPI Application Entrypoint

This is the main entrypoint for the CivicMind AI FastAPI application.
It initializes the FastAPI instance, configures middleware, registers routers,
and defines root-level endpoints.

FASTAPI APPLICATION LIFECYCLE:
When you run this application (e.g., uvicorn main:app --reload):
1. Python executes this file from top to bottom
2. FastAPI() is instantiated, creating the ASGI application
3. Routers are registered, mounting their routes at specified paths
4. Middleware is configured (CORS, authentication, etc.)
5. Uvicorn (ASGI server) starts and serves the application
6. On each request, FastAPI matches the URL to a registered handler
"""

from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config import settings
from api.health import router as health_router

from api.coordinator import router as coordinator_router


# =============================================================================
# FASTAPI APPLICATION INITIALIZATION
# =============================================================================
# WHAT IS FastAPI()?
# FastAPI is a modern, fast (high-performance) Python web framework for building
# APIs with Python based on standard Python type hints. The FastAPI() class
# creates an ASGI (Asynchronous Server Gateway Interface) application instance.
#
# Key features:
# - Automatic API documentation (Swagger UI and ReDoc at /docs and /redoc)
# - Type validation using Pydantic models
# - Async/await support for high concurrency
# - Dependency injection system
# - Built on Starlette for performance

app = FastAPI(
    # Application title appears in auto-generated docs
    title=settings.APP_NAME,
    # Version impacts API documentation and client caching
    version=settings.API_VERSION,
    # Description shown in API documentation
    description="Multi-Agent Community Decision Intelligence Platform API",
    # Contact information for API consumers
    contact={
        "name": "CivicMind AI Team",
        "url": "https://github.com/civicmind-ai/civicmind",
    },
    # License information
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    # OpenAPI URL for documentation generation
    openapi_url="/openapi.json",
    # Docs URL path
    docs_url="/docs" if settings.DEBUG else None,
    # Redoc URL path (alternative documentation UI)
    redoc_url="/redoc" if settings.DEBUG else None,
)


# =============================================================================
# ROUTER REGISTRATION
# =============================================================================
# WHAT ARE ROUTERS?
# FastAPI's APIRouter allows you to organize related endpoints into separate
# modules. Instead of defining all routes in this single file, routers let you:
# - Group endpoints by domain (users, health, analytics, etc.)
# - Share common path prefixes and tags
# - Create reusable, self-contained route modules
# - Test routes in isolation

# Register the health router with a URL prefix
# This means all routes defined in health.py will be prefixed with /api/v1
# Example: health.py defines /health, accessible at /api/v1/health
app.include_router(
    health_router,
    prefix="/api/v1"
)


app.include_router(
    coordinator_router,
    prefix="/api/v1",
    tags=["Coordinator"]
)
# =============================================================================
# ROOT ENDPOINT
# =============================================================================
# The root endpoint (GET /) serves as the landing page for the API.
# Common uses:
# - API discovery: Returns basic info about the service
# - Load balancer health checks: Simple ping endpoint
# - Documentation redirect: Can redirect to /docs
# - Service identification: Helps developers confirm they are hitting the right service

@app.get(
    "/",
    response_class=JSONResponse,
    summary="Root endpoint",
    description="Returns a welcome message for the CivicMind AI API"
)

async def root() -> dict[str, Any]:
    """
    Root endpoint returning a welcome message.

    This endpoint serves as the API entrypoint and landing URL.
    It provides a simple, friendly response confirming the API is running
    and directs users to the documentation.

    Returns:
        dict[str, str]: JSON response containing:
            - message: Welcome message string
            - version: Current API version
            - docs_url: Link to API documentation

    Example:
        >>> requests.get("http://localhost:8000/").json()
        {
            "message": "Welcome to CivicMind AI",
            "version": "1.0.0",
            "docs_url": "/docs"
        }
    """
    return {
        "message": "Welcome to CivicMind AI",
        "version": settings.API_VERSION,
        "docs_url": "/docs" if settings.DEBUG else None
    }


# =============================================================================
# APPLICATION ENTRYPOINT
# =============================================================================
# This allows running the app directly with: python main.py
# In production, use: uvicorn main:app --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    
    # Running here only when executed directly (not imported)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
