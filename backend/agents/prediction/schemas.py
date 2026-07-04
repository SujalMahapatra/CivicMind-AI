from pydantic import BaseModel, Field, ConfigDict


class PredictionRequest(BaseModel):
    """
    Request model for time-series forecasting.
    """

    file_path: str = Field(
        ...,
        min_length=1,
        description="Path to dataset file"
    )

    target_column: str = Field(
        ...,
        min_length=1,
        description="Column to forecast"
    )

    forecast_days: int = Field(
        ...,
        gt=0,
        le=30,
        description="Number of future values to predict"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "file_path": "../datasets/air_quality.csv",
                "target_column": "aqi",
                "forecast_days": 7
            }
        }
    )


class PredictionResponse(BaseModel):
    """
    Response model for forecasting results.
    """

    file_name: str

    target_column: str

    forecast_days: int

    predictions: list[float]

    model_used: str

    r2_score: float

    trend_direction: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "file_name": "air_quality.csv",
                "target_column": "aqi",
                "forecast_days": 7,
                "predictions": [
                    180.5,
                    184.2,
                    188.0
                ],
                "model_used": "LinearRegression"
            }
        }
    )