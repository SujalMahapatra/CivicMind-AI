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
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from schemas import AnalysisRequest, AnalysisResponse
from agent import AnalyticsAgent


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
    summary="Analyze a dataset and return statistics",
    description="""
    Performs comprehensive analysis on a dataset file.
    
    The Analytics Agent:
    1. Validates the file exists at the specified path
    2. Loads the dataset (supports CSV, JSON, Parquet formats)
    3. Calculates row/column counts
    4. Identifies numeric vs categorical columns
    5. Counts missing values and duplicate rows
    6. Computes an overall data quality score
    
    The data quality score (0-100) considers:
    - Completeness: Percentage of non-missing values
    - Uniqueness: Absence of duplicate rows
    - Validity: Proper data types in each column
    
    If the file cannot be found or has invalid format, appropriate
    HTTP errors are returned with descriptive messages.
    """,
    response_description="""
    Comprehensive dataset analysis including:
    - Dataset dimensions (rows, columns)
    - Data quality metrics (missing values, duplicates)
    - Column type distribution
    - Overall data quality score
    """,
)
async def analyze_dataset(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze a dataset file and return statistical summary.
    
    This endpoint is the primary interface for data analysis in CivicMind AI.
    It accepts a file path to a dataset and returns comprehensive statistics
    useful for understanding data quality and structure.
    
    Args:
        request: AnalysisRequest containing:
            - file_path: Path to the dataset file (relative to project root)
            
    Returns:
        AnalysisResponse containing:
            - rows: Total number of data rows
            - columns: Total number of columns
            - missing_values: Count of missing cells
            - duplicate_rows: Count of duplicate rows
            - numeric_columns: Count of numeric columns
            - categorical_columns: Count of categorical/text columns
            - data_quality_score: Overall quality (0.0-100.0)
            
    Raises:
        HTTPException: 
            - 400: File path is invalid or not a string
            - 404: File does not exist at path
            - 422: File exists but has malformed data
            - 500: Analysis computation failed unexpectedly
            
    Example Request:
        {
            "file_path": "datasets/community_health_data.csv"
        }
        
    Example Success Response:
        {
            "rows": 12500,
            "columns": 18,
            "missing_values": 45,
            "duplicate_rows": 2,
            "numeric_columns": 12,
            "categorical_columns": 6,
            "data_quality_score": 98.2
        }
        
    Supported File Formats:
        - CSV (.csv): Comma-separated values
        - JSON (.json): JavaScript Object Notation
        - Parquet (.parquet): Apache Parquet format
        - Excel (.xlsx): Microsoft Excel (if openpyxl installed)
        
    Data Quality Score Calculation:
        score = (completeness * 0.4) + (uniqueness * 0.3) + (validity * 0.3)
        
        Where:
        - completeness = 100 - (% of missing values)
        - uniqueness = 100 - (% of duplicate rows)
        - validity = percentage of columns with correct types
    """
    file_path: str = request.file_path
    
    # =============================================================================
    # INPUT VALIDATION
    # =============================================================================
    # Step 1: Validate file path is not empty
    if not file_path or not file_path.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File path cannot be empty"
        )
    
    # Step 2: Validate file path is a string (Pydantic handles this, but defensive)
    if not isinstance(file_path, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File path must be a string, got {type(file_path).__name__}"
        )
    
    # Step 3: Convert to Path object and validate
    # Path validates the file system path and handles different OS path formats
    try:
        path_obj = Path(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file path format: {str(e)}"
        )
    
    # Step 4: Check file exists
    if not path_obj.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset file not found: '{file_path}'"
        )
    
    # Step 5: Verify it's a file (not a directory)
    if not path_obj.is_file():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Path is not a file: '{file_path}'"
        )
    
    # =============================================================================
    # DATA ANALYSIS
    # =============================================================================
    try:
        # Delegate analysis to the Analytics Agent
        # The agent encapsulates the analysis logic and handles various file formats
        analysis_result: AnalysisResponse = analytics_agent.analyze(request)
        
        return analysis_result
        
    except FileNotFoundError:
        # Should not reach here due to validation above, but defensive coding
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset file not accessible: '{file_path}'"
        )
        
    except ValueError as e:
        # Raised for malformed data (e.g., corrupted CSV, invalid JSON)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dataset validation failed: {str(e)}"
        )
        
    except PermissionError:
        # Raised if file exists but no read permissions
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied reading file: '{file_path}'"
        )
        
    except Exception as e:
        # Catch-all for unexpected errors
        # In production, log this to an error tracking service (Sentry, etc.)
        print(f"Unexpected error analyzing dataset: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed unexpectedly. Please try again or contact support."
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
