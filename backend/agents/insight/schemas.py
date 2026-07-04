from pydantic import BaseModel, Field, ConfigDict


class InsightRequest(BaseModel):
    """
    Request model for Gemini-powered insight generation.
    """

    domain: str = Field(
        ...,
        description="Community domain being analyzed"
    )

    analytics_summary: str = Field(
        ...,
        min_length=1
    )

    prediction_summary: str = Field(
        ...,
        min_length=1
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "domain": "environment",
                "analytics_summary":
                    "Dataset contains 1000 rows with 95 quality score.",
                "prediction_summary":
                    "AQI expected to increase from 180 to 220."
            }
        }
    )


class InsightResponse(BaseModel):
    """
    Gemini-generated insights.
    """

    domain: str

    insights: str

    model_used: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "domain": "environment",
                "insights":
                    "Air quality is expected to worsen steadily.",
                "model_used": "gemini-2.5-flash"
            }
        }
    )