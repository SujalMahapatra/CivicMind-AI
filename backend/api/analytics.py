"""
CivicMind AI - Analytics Router

This module provides the HTTP endpoints for the Analytics Agent.
The Analytics Agent is responsible for data analysis operations including
statistical summaries, data quality assessments, and exploratory data analysis.

ENDPOINT DOCUMENTATION:
    POST /analytics/analyze
        - Receives a file path to a dataset
        - Performs comprehensive data analysis
        - Returns statistical summary and data quality metrics

BEST PRACTICES:
    - Validation: All file paths validated before processing
    - Error Handling: Specific exceptions with HTTP status codes
    - Response Models: Pydantic schemas ensure consistent API responses
    - Documentation: Auto-generated OpenAPI docs via FastAPI decorators

EXAMPLE USAGE:
    >>> import requests
    >>> response = requests.post(
    ...     "http://localhost:8000/analytics/analyze",
    ...     json={"file_path": "datasets/community_health_data.csv"}
    ... )
    >>> print(response.json())
    {
        "rows": 10000,
        "columns": 15,
        "missing_values": 23,
        "duplicate_rows": 5,
        "numeric_columns": 10,
        "categorical_columns": 5,
        "data_quality_score": 97.8
    }
"""

from pathlib import Path


from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse


from agents.analytics.schemas import (
    AnalysisResponse,
)

from agents.analytics.analytics_agent import (
    AnalyticsAgent,
)

from fastapi import UploadFile, File

from pathlib import Path
import shutil




# =============================================================================
# ROUTER INITIALIZATION
# =============================================================================
# APIRouter groups all analytics-related endpoints under the /analytics prefix.
# This creates a clean URL structure: /analytics/analyze, /analytics/summary, etc.
# The 'tags' parameter groups these endpoints in the Swagger UI documentation.


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    # Default responses for common error scenarios
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request - malformed file path"},
        status.HTTP_404_NOT_FOUND: {"description": "File not found at specified path"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error - invalid data format"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error during analysis"},
    },
)

# =============================================================================
# ANALYTICS AGENT INSTANCE
# =============================================================================
# The AnalyticsAgent is instantiated once at module level (singleton pattern).
# Benefits:
# - Performance: No per-request instantiation
# - Resource sharing: Reuses connections to data sources
# - Consistency: All requests use same agent configuration
#
# For production, consider using FastAPI's Depends() with yield for:
# - Database connections that need cleanup
# - External API clients with rate limiting
# - Resources requiring explicit lifecycle management

analytics_agent: AnalyticsAgent = AnalyticsAgent()


# =============================================================================
# ANALYZE ENDPOINT
# =============================================================================
# This is the primary endpoint for data analysis requests.
# It receives a file path, validates it, and returns comprehensive statistics.

@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze uploaded dataset",
    description="Upload a dataset file and return analysis results."
)
async def analyze_dataset(
    file: UploadFile = File(...)
) -> AnalysisResponse:
    """
    Analyze an uploaded dataset.

    Supported formats:
    - CSV (.csv)
    - JSON (.json)
    - Excel (.xlsx)

    Workflow:
    1. Receive uploaded file
    2. Save temporarily in uploads/
    3. Pass file path to AnalyticsAgent
    4. Return analysis results
    """

    try:
        # ---------------------------------------------------------------------
        # Validate uploaded file
        # ---------------------------------------------------------------------
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file uploaded"
            )

        # ---------------------------------------------------------------------
        # Create uploads directory
        # ---------------------------------------------------------------------
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)

        # ---------------------------------------------------------------------
        # Save uploaded file
        # ---------------------------------------------------------------------
        file_path = uploads_dir / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------------------------------------------------------------
        # Run analysis
        # ---------------------------------------------------------------------
        result = analytics_agent.analyze(
            str(file_path)
        )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied while reading uploaded file"
        )

    except Exception as e:
        print(f"Unexpected error analyzing dataset: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dataset analysis failed"
        )



# =============================================================================
# OPTIONAL: SUMMARY ENDPOINT (Simplified Analysis)
# =============================================================================
# You can uncomment this for a lightweight version that only returns
# basic counts without detailed quality metrics.

# @router.post(
#     "/analyze/summary",
#     response_model=AnalysisSummaryResponse,
#     summary="Quick dataset summary",
#     description="Returns only basic row count without detailed analysis",
# )
# async def analyze_summary(request: AnalysisRequest) -> AnalysisSummaryResponse:
#     """Quick summary endpoint for fast previews."""
#     path_obj = Path(request.file_path)
#     if not path_obj.exists():
#         raise HTTPException(status_code=404, detail="File not found")
#     
#     return analytics_agent.analyze_summary(request)


# =============================================================================
# DEPENDENCY INJECTION ALTERNATIVE (Production Pattern)
# =============================================================================
# For production, you might want to use FastAPI's dependency injection:
# 
# from fastapi import Depends
# 
# async def get_analytics_agent() -> AnalyticsAgent:
#     """Dependency to get analytics agent instance."""
#     return analytics_agent
# 
# @router.post("/analyze")
# async def analyze_with_di(
#     request: AnalysisRequest,
#     agent: AnalyticsAgent = Depends(get_analytics_agent)
# ) -> AnalysisResponse:
#     """Version using dependency injection."""
#     return agent.analyze(request)
