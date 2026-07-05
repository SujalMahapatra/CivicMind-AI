"""
CivicMind AI - Insight Agent

This module implements the Insight Agent for CivicMind AI.

## PURPOSE:

The Insight Agent converts structured outputs from:

* Analytics Agent
* Prediction Agent

into human-readable decision intelligence using Gemini.

## WHY THIS AGENT EXISTS:

Analytics Agent answers:

```
"What happened?"
```

Prediction Agent answers:

```
"What may happen next?"
```

Insight Agent answers:

```
"What does it mean?"
```

The Insight Agent acts as the bridge between data analysis and
decision-making.

## WORKFLOW:

Analytics Results
+
Prediction Results
↓
Insight Agent
↓
Gemini Service
↓
Actionable Insights

## ARCHITECTURE:

The Insight Agent does NOT directly communicate with Gemini.

Instead it uses:

```
gemini_service.generate_text()
```

This keeps all Gemini-related logic centralized in a single service layer.
"""

from services.gemini_service import (
    gemini_service,
    GeminiService
)

from .schemas import (
    InsightRequest,
    InsightResponse
)

class InsightAgent:
    """
    Insight Agent for CivicMind AI.

    ```
    Generates human-readable insights from analytics
    and prediction summaries.

    Responsibilities:
    -----------------
    - Build a structured prompt
    - Send prompt to Gemini Service
    - Return generated insights

    Non-Responsibilities:
    ---------------------
    - Data analytics
    - Forecast generation
    - Direct Gemini SDK interaction
    """

    def _build_insight_prompt(
        self,
        domain: str,
        analytics_summary: str,
        prediction_summary: str
    ) -> str:
        """
        Build a structured prompt for Gemini.

        Why prompt engineering matters:
        -------------------------------
        Large Language Models perform significantly better when given:

        - Clear role definition
        - Context
        - Structured tasks
        - Output expectations

        This prompt helps Gemini generate consistent
        decision-intelligence insights.
        """

        return f"""
    ```

    You are an expert Community Decision Intelligence Analyst.

    DOMAIN:
    {domain}

    ANALYTICS SUMMARY:
    {analytics_summary}

    PREDICTION SUMMARY:
    {prediction_summary}

    Based ONLY on the information above, generate a concise decision-intelligence report.

    Include:

    1. Key Findings
    2. Emerging Risks
    3. Important Trends
    4. Community Impact

    Requirements:

    * Be concise and actionable.
    * Use simple language.
    * Focus on decision-making.
    * Do not invent information.
    * Base conclusions only on the provided summaries.
    """

    def generate_insights(
            self,
            request: InsightRequest
        ) -> InsightResponse:
        """
        Generate AI-powered insights.

        ```
            Args:
                request:
                    InsightRequest containing:
                    - domain
                    - analytics_summary
                    - prediction_summary

            Returns:
                InsightResponse
            """

        if request is None:
            raise ValueError(
                "InsightRequest cannot be None."
            )

        if not request.analytics_summary.strip():
            raise ValueError(
                "analytics_summary cannot be empty."
            )

        if not request.prediction_summary.strip():
            raise ValueError(
                "prediction_summary cannot be empty."
            )

        prompt: str = self._build_insight_prompt(
            domain=request.domain,
            analytics_summary=request.analytics_summary,
            prediction_summary=request.prediction_summary
        )

        try:
            insights: str = gemini_service.generate_text(
                prompt=prompt
            )

            return InsightResponse(
                domain=request.domain,
                insights=insights,
                model_used=GeminiService.DEFAULT_MODEL
            )

        except Exception as e:
            raise Exception(
                f"Failed to generate insights: {str(e)}"
            ) from e
    
