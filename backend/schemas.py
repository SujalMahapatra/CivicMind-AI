"""
CivicMind AI - Pydantic Schemas

This module defines all Pydantic data models used throughout the CivicMind AI
application. Pydantic provides data validation and settings management using
Python type hints, making it easy to define data structures that are both
validatable and serializable.

PYDANTIC V2 BEST PRACTICES:
--------------------------
This file follows Pydantic V2 syntax patterns:

1. ConfigDict: Use model_config = ConfigDict(...) instead of class Config
2. Field Validation: Use Field() for constraints, descriptions, and examples
3. Type Hints: Always specify field types for IDE support and validation
4. Enums: Use Python Enums for constrained string values
5. JSON Schema: Use json_schema_extra for OpenAPI documentation

EDUCATIONAL NOTES:
----------------
- BaseModel: Core class for creating data schemas with validation
- Field: Adds metadata, constraints, and validation rules
- ConfigDict: Model-level configuration options
- Validation: Pydantic validates data automatically on instantiation
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# =============================================================================
# ENUMERATIONS
# =============================================================================
# Enums define a fixed set of named values. Using enums instead of plain
# strings ensures type safety, allows IDE autocomplete, and prevents invalid
# values from being passed at runtime.

class Domain(Enum):
    """Domain categories for CivicMind AI queries."""
    health = "health"
    environment = "environment"
    mobility = "mobility"
    unknown = "unknown"


class Intent(Enum):
    """User intent categories for CivicMind AI queries."""
    analytics = "analytics"
    prediction = "prediction"
    recommendation = "recommendation"
    report = "report"
    knowledge = "knowledge"
    unknown = "unknown"


# =============================================================================
# REQUEST MODELS (Input Validation)
# =============================================================================
# Request models validate incoming API data before processing.


class RouteRequest(BaseModel):
    """
    Request model for routing a user query to the appropriate agent.
    
    Captures the raw user input that needs to be analyzed and routed
    to specialized agents based on domain and intent classification.
    """
    query: str = Field(
        ...,  # Required field (no default)
        min_length=1,
        max_length=10000,
        description="Natural language query from the user"
    )
    
    model_config: ConfigDict = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "query": "Predict air quality for tomorrow"
            }
        }
    )


class AnalysisRequest(BaseModel):
    """
    Request model for dataset analysis operations.
    
    This model captures the file path of a dataset that needs to be
    analyzed by the Analytics Agent. The agent loads the file and
    computes comprehensive statistics and data quality metrics.
    
    Attributes:
        file_path: Path to the dataset file (relative or absolute)
        
    Supported Formats:
        - CSV (.csv): Comma-separated values with headers
        - JSON (.json): Array of objects or nested structure
        - Parquet (.parquet): Apache Parquet columnar format
        
    Validation Rules:
        - file_path: Non-empty string, min 1 char
        - Cannot be null or empty
    """
    
    file_path: str = Field(
        ...,  # Ellipsis means this field is REQUIRED (no default value)
        min_length=1,
        description="Path to the dataset file for analysis"
    )
    
    model_config: ConfigDict = ConfigDict(
        # Automatically strip whitespace from strings
        str_strip_whitespace=True,
        # OpenAPI documentation example
        json_schema_extra={
            "example": {
                "file_path": "datasets/sample.csv"
            }
        }
    )


# =============================================================================
# RESPONSE MODELS (Output Schemas)
# =============================================================================
# Response models define the structure of API responses for consistent
# client-side consumption and automatic OpenAPI documentation generation.


class RouteResponse(BaseModel):
    """
    Response model for query routing decisions.
    
    Contains routing information indicating which specialized agent
    should handle a user query based on domain and intent classification.
    """
    domain: Domain
    intent: Intent
    target_agent: str
    confidence: float
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "domain": "environment",
                "intent": "prediction",
                "target_agent": "prediction_agent",
                "confidence": 0.9
            }
        }
    )


class AnalysisResponse(BaseModel):
    """
    Response model containing dataset analysis results.
    
    This model represents a comprehensive statistical summary of a dataset,
    including dimensions, data quality metrics, column type distribution,
    and an overall quality score.
    
    Attributes:
        rows: Total number of data rows (excluding header)
        columns: Total number of columns/features
        missing_values: Total count of null/empty cells
        duplicate_rows: Count of exact duplicate rows
        numeric_columns: Number of numeric data type columns
        categorical_columns: Number of text/category columns
        data_quality_score: Overall quality score (0.0-100.0)
        
    Data Quality Score:
        Score from 0.0 (poor) to 100.0 (excellent).
        Calculated from:
        - Completeness: Percentage of non-missing values (40% weight)
        - Uniqueness: Absence of duplicate rows (30% weight)
        - Validity: Proper data types and formats (30% weight)
    """
    
    rows: int = Field(
        ...,  # Required
        ge=0,  # Greater than or equal to 0 (cannot be negative)
        description="Total number of data rows"
    )
    
    columns: int = Field(
        ...,
        ge=0,
        description="Total number of columns/features"
    )
    
    missing_values: int = Field(
        ...,
        ge=0,
        description="Total count of missing/null values"
    )
    
    duplicate_rows: int = Field(
        ...,
        ge=0,
        description="Count of exact duplicate rows"
    )
    
    numeric_columns: int = Field(
        ...,
        ge=0,
        description="Number of numeric columns (int, float, decimal)"
    )
    
    categorical_columns: int = Field(
        ...,
        ge=0,
        description="Number of categorical/text columns"
    )
    
    data_quality_score: float = Field(
        ...,
        ge=0.0,  # Must be >= 0.0
        le=100.0,  # Must be <= 100.0
        description="Overall data quality score from 0.0 to 100.0"
    )
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "rows": 1000,
                "columns": 12,
                "missing_values": 14,
                "duplicate_rows": 1,
                "numeric_columns": 8,
                "categorical_columns": 4,
                "data_quality_score": 98.5
            }
        }
    )


class InsightRequest(BaseModel):
    """
    Request model for generating actionable insights from analytics data.
    
    The InsightRequest encapsulates all data needed to generate human-readable
    insights from statistical summaries and predictions. It serves as input
    to the Insight Agent which uses AI to synthesize decision intelligence.
    
    Attributes:
        domain: Subject domain (health, environment, mobility)
        analytics_summary: Statistical analysis results in structured format
        prediction_summary: Forecast results and trend predictions
        
    Usage:
        >>> request = InsightRequest(
        ...     domain=Domain.health,
        ...     analytics_summary={"hospitals": 15, "patients": 1200},
        ...     prediction_summary={"forecast": "+5% next quarter"}
        ... )
    """
    
    domain: Domain = Field(
        ...,  # Required
        description="Subject domain for the insight (health, environment, mobility)"
    )
    
    analytics_summary: str = Field(
        ...,  # Required
        min_length=1,
        max_length=50000,
        description="Structured analytics summary (tables, metrics, statistics)"
    )
    
    prediction_summary: str = Field(
        ...,  # Required
        min_length=1,
        max_length=50000,
        description="Prediction results, forecasts, and trend analysis"
    )
    
    model_config: ConfigDict = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "domain": "health",
                "analytics_summary": "15 hospitals, 1200 patients, 95% capacity",
                "prediction_summary": "Patient volume expected to increase 5% next quarter"
            }
        }
    )


class InsightResponse(BaseModel):
    """
    Response model containing AI-generated decision intelligence insights.
    
    The Insight Agent transforms raw analytics into actionable insights organized
    into four key areas: what the data shows (findings), potential problems
    (risks), directional patterns (trends), and community relevance (impact).
    
    Attributes:
        key_findings: Insights from the analytics data
        emerging_risks: Identified concerns that need attention
        important_trends: Pattern observations and directional indicators
        community_impact: How findings affect the community
        model_used: Gemini model version that generated the insights
        
    Usage:
        >>> response = InsightResponse(
        ...     key_findings="Hospital capacity at 95%"
        ... )
    """
    
    key_findings: str = Field(
        ...,  # Required
        min_length=1,
        description="Primary insights derived from analytics and predictions"
    )
    
    emerging_risks: str = Field(
        ...,  # Required
        min_length=1,
        description="Potential concerns or risks identified in the data"
    )
    
    important_trends: str = Field(
        ...,  # Required
        min_length=1,
        description="Directional patterns and trend observations"
    )
    
    community_impact: str = Field(
        ...,  # Required
        min_length=1,
        description="Impact on community stakeholders and public welfare"
    )
    
    model_used: str = Field(
        "gemini-2.5-flash",
        description="Gemini model version used for generating insights"
    )
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "key_findings": "Hospital capacity at 95%. Emergency wait times increased 15%.",
                "emerging_risks": "Capacity shortage risk within 2 months. Staff burnout indicators.",
                "important_trends": "Consistent 3% monthly growth in patient volume.",
                "community_impact": "Community may face longer wait times and reduced care availability.",
                "model_used": "gemini-2.5-flash"
            }
        }
    )


class RecommendationRequest(BaseModel):
    """
    Request model for generating actionable recommendations.
    
    The RecommendationRequest encapsulates insights from the Insight Agent
    that need to be converted into specific, actionable recommendations
    for community stakeholders and decision-makers.
    
    Attributes:
        domain: Subject domain (health, environment, mobility)
        insights: AI-generated insights including findings, risks, trends, impact
        
    Usage:
        >>> request = RecommendationRequest(
        ...     domain=Domain.environment,
        ...     insights="Air quality declining. AQI forecast to reach 120."
        ... )
    """
    
    domain: Domain = Field(
        ...,  # Required
        description="Subject domain for recommendations (health, environment, mobility)"
    )
    
    insights: str = Field(
        ...,  # Required
        min_length=1,
        max_length=50000,
        description="AI-generated insights to convert into recommendations"
    )
    
    model_config: ConfigDict = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "domain": "environment",
                "insights": "Air quality declining. AQI forecast to reach 120. Community health impact expected."
            }
        }
    )


class RecommendationResponse(BaseModel):
    """
    Response model containing actionable recommendations.
    
    The Recommendation Agent converts insights into three categories of
    recommendations covering immediate response, preventive measures, and
    long-term strategic planning.
    
    Attributes:
        immediate_actions: Steps to take right now
        preventive_actions: Steps to prevent problems
        long_term_actions: Strategic initiatives
        model_used: Gemini model version
    """
    
    immediate_actions: str = Field(
        ...,  # Required
        min_length=1,
        description="Immediate response actions (what to do now)"
    )
    
    preventive_actions: str = Field(
        ...,  # Required
        min_length=1,
        description="Preventive actions (how to stop problems before they start)"
    )
    
    long_term_actions: str = Field(
        ...,  # Required
        min_length=1,
        description="Long-term strategic actions (sustainable solutions)"
    )
    
    model_used: str = Field(
        "gemini-2.5-flash",
        description="Gemini model version used"
    )
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "immediate_actions": "Issue air quality alerts. Recommend N95 masks. Postpone outdoor events.",
                "preventive_actions": "Increase public transit subsidies. Establish car-free zones. Plant green buffers.",
                "long_term_actions": "Transition to electric buses. Build urban forests. Implement congestion pricing.",
                "model_used": "gemini-2.5-flash"
            }
        }
    )
