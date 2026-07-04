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



from pydantic import BaseModel, Field, ConfigDict






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
        - Excel (.xlsx): Microsoft Excel files with multiple sheets
        
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

        Calculation:

        score = 100

        score -= missing_percentage * 50
        score -= duplicate_percentage * 25

        The final score is clamped between 0 and 100.

        Higher scores indicate cleaner and more reliable datasets.
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

    file_name: str = Field(
        ...,
        description="Dataset file name"
    )
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "file_name": "air_quality.csv",
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
