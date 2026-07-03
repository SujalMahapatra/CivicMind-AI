"""
CivicMind AI - Health Check Router

This module provides health check endpoints for monitoring and orchestration systems.

WHAT IS APIRouter?
APIRouter is a FastAPI class that allows you to organize routes into separate modules
rather than declaring all endpoints in a single main.py file. Think of it as a mini
FastAPI application that you can "plug into" the main app. Benefits include:
- Separation of concerns: Each router handles a specific domain (auth, users, health)
- Reusability: Same router can be mounted at different paths or in different apps
- Better maintainability: Smaller, focused files are easier to understand and test
- Team collaboration: Different developers can work on different routers independently

WHY HEALTH ENDPOINTS EXIST?
Health checks answer the question: "Is this service healthy and able to handle requests?"
They serve as a simple ping mechanism that confirms:
- The application process is running
- The HTTP server is accepting requests
- Critical dependencies (databases, external APIs) are accessible
- The service is ready to receive traffic

HOW MONITORING SYSTEMS USE HEALTH CHECKS:
- Load Balancers: Route traffic only to healthy instances
- Kubernetes: Uses liveness probes to restart unhealthy pods
- Docker: Determines if a container should be recreated
- Uptime Monitoring: Services like Pingdom/PagerDuty alert when health checks fail
- Deployment Pipelines: Prevent new versions from going live if health checks fail
- Service Meshes: Automatically remove failing instances from the mesh
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from config import settings


# =============================================================================
# APIRouter SETUP
# =============================================================================
# Create a router instance. The 'tags' parameter groups endpoints in auto-generated
docs (Swagger UI). The 'prefix' could be added here (e.g., "/health"), but we
define the full path in the decorator for clarity and flexibility.
router = APIRouter(
    tags=["Health"]
)


# =============================================================================
# PYDANTIC MODELS
# =============================================================================
# Using Pydantic models ensures API documentation is complete and responses
# are validated. This provides automatic OpenAPI schema generation.

class HealthResponse(BaseModel):
    """
    Standard health check response schema.

    Attributes:
        status: Current health status ('healthy' or 'unhealthy')
        service: Name of the service reporting health
        version: Current API version string
        timestamp: ISO 8601 timestamp when the check was performed
        environment: Current deployment environment
    """
    status: str
    service: str
    version: str
    timestamp: str
    environment: str

    # Pydantic V2 configuration for better JSON serialization
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "service": "CivicMind AI",
                "version": "v1",
                "timestamp": "2024-01-15T10:30:00Z",
                "environment": "production"
            }
        }
    }


# =============================================================================
# HEALTH CHECK ENDPOINT
# =============================================================================

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Returns the current health status of the CivicMind AI service",
    response_description="Service health status and metadata"
)
async def health_check() -> HealthResponse:
    """
    Perform a health check on the CivicMind AI service.

    This endpoint performs lightweight health validation and returns the current
    status of the application. It does NOT perform deep health checks (like
    database connectivity) to ensure fast responses for load balancers.

    Returns:
        HealthResponse: A response indicating the service is healthy, including:
            - status: "healthy"
            - service: Application name from configuration
            - version: API version string (v{major})
            - timestamp: Current UTC timestamp
            - environment: Current deployment environment

    Example:
        >>> requests.get("http://api/health").json()
        {
            "status": "healthy",
            "service": "CivicMind AI",
            "version": "v1",
            "timestamp": "2024-01-15T10:30:00Z",
            "environment": "production"
        }

    Raises:
        HTTPException: If the service is unhealthy (500 status code)
    """
    # Note: This is a basic "liveness" check. In production, you might want to:
    # 1. Check database connectivity (deep health check)
    # 2. Check external API dependencies
    # 3. Check disk space, memory usage
    # 4. Query critical background job status
    # Consider adding a /health/ready endpoint for deep checks

    return HealthResponse(
        status="healthy",
        service=settings.APP_NAME,
        version=f"v{settings.API_VERSION.split('.')[0]}",
        timestamp=datetime.utcnow().isoformat() + "Z",
        environment=settings.ENVIRONMENT
    )


# =============================================================================
# OPTIONAL: DEEP HEALTH CHECK
# =============================================================================
# Uncomment and implement if you need to check database connections

# @router.get(
#     "/health/ready",
#     response_model=HealthResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Readiness health check",
#     description="Returns detailed health status including database connectivity"
# )
# async def readiness_check() -> HealthResponse:
#     """
#     Perform a deep health check including dependency validation.
#
#     This endpoint checks all critical dependencies (database, external APIs, etc.)
#     and should be used by orchestration systems to determine if the service is
#     ready to receive traffic. 
#
#     Returns:
#         HealthResponse: Detailed health information
#
#     Raises:
#         HTTPException: If any critical dependency is unhealthy
#     """
#     # Example: Check database connection
#     # try:
#     #     db.is_connected()
#     # except Exception:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#     #         detail="Database connection failed"
#     #     )
#
#     return HealthResponse(...)
