from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

from sklearn.metrics import r2_score

from .schemas import PredictionResponse


class PredictionAgent:
    """
    Generic Time-Series Prediction Agent.

    Uses Linear Regression to forecast future values from
    sequential historical data.

    Examples:
        AQI Forecasting
        Traffic Forecasting
        Energy Consumption Forecasting
        Hospital Visit Forecasting
    """

    def load_dataset(self, file_path: str) -> pd.DataFrame:
        """
        Load dataset into a pandas DataFrame.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".csv":
            return pd.read_csv(path)

        elif extension == ".xlsx":
            return pd.read_excel(path)

        elif extension == ".json":
            return pd.read_json(path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )
    
    def prepare_features(
        self,
        df: pd.DataFrame,
        target_column: str
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Convert dataframe into X and y for training.
        """

        if target_column not in df.columns:
            raise ValueError(
                f"Column '{target_column}' not found"
            )
        
        if df[target_column].isnull().any():
            raise ValueError(
                f"Target column '{target_column}' contains missing values"
            )

        if not pd.api.types.is_numeric_dtype(
            df[target_column]
        ):
            raise ValueError(
                f"Target column '{target_column}' must be numeric"
            )
        if df[target_column].isnull().any():
            raise ValueError(
                f"Target column '{target_column}' contains missing values"
            )

        y = df[target_column].values

        X = np.arange(len(y)).reshape(-1, 1)

        return X, y
    
    def train_model(
        self,
        X : np.ndarray,
        y : np.ndarray
    ) -> LinearRegression:
        """
        Train Linear Regression model.
        """

        model = LinearRegression()

        model.fit(X, y)

        y_pred = model.predict(X)

        score = round(float(r2_score(y, y_pred)), 4)

        return model,score
    
    def predict_future(
        self,
        model: LinearRegression,
        total_rows: int,
        forecast_days: int
    ) -> list[float]:
            """
            Generate future predictions.
            """

            future_X = np.arange(
                total_rows,
                total_rows + forecast_days
            ).reshape(-1, 1)

            predictions = model.predict(future_X)

            return [
                round(float(value), 2)
                for value in predictions
            ]
        
    def predict(
        self,
        file_path: str,
        target_column: str,
        forecast_days: int
    ) -> PredictionResponse:
            """
            Main prediction workflow.
            """

            df = self.load_dataset(file_path)

            X, y = self.prepare_features(
                df,
                target_column
            )

            model, r2_score = self.train_model(X, y)

            predictions = self.predict_future(
                model,
                len(df),
                forecast_days
            )
            if predictions[-1] > predictions[0]:
                trend_direction = "Increasing"
            elif predictions[-1] < predictions[0]:
                trend_direction = "Decreasing"
            else:
                trend_direction = "Stable"

            return PredictionResponse(
                file_name=Path(file_path).name,
                target_column=target_column,
                forecast_days=forecast_days,
                predictions=predictions,
                trend_direction=trend_direction,
                model_used="LinearRegression",
                r2_score=r2_score
            )