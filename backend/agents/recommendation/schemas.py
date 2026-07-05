from pydantic import BaseModel, Field, ConfigDict


class RecommendationRequest(BaseModel):

    domain: str = Field(...)

    insights: str = Field(...)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "domain": "environment",
                "insights": "AQI expected to increase."
            }
        }
    )


class RecommendationResponse(BaseModel):

    domain: str

    recommendations: str

    model_used: str