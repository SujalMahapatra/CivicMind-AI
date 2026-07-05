"""
CivicMind AI - Recommendation Agent

## PURPOSE:

The Recommendation Agent converts AI-generated insights into
actionable recommendations for stakeholders.

## WORKFLOW:

Analytics
↓
Prediction
↓
Insight Agent
↓
Recommendation Agent
↓
Decision Support

The Recommendation Agent answers:

"What should we do next?"
"""

from services.gemini_service import (
    gemini_service,
    GeminiService
)

from .schemas import (
    RecommendationRequest,
    RecommendationResponse
)

class RecommendationAgent:
    """
    Generates actionable recommendations from AI insights.
    """

    
    def _build_recommendation_prompt(
        self,
        domain: str,
        insights: str
    ) -> str:
        """
        Build recommendation prompt.
        """

        return f"""
    ```

    You are an expert Community Decision Advisor.

    DOMAIN:
    {domain}

    INSIGHTS:
    {insights}

    Based ONLY on the information above, generate actionable recommendations.

    Include:

    1. Immediate Actions
    2. Preventive Actions
    3. Long-Term Strategic Actions

    Requirements:

    * Be practical.
    * Be specific.
    * Focus on decision-making.
    * Avoid generic advice.
    * Keep recommendations concise.
    """

    def generate_recommendations(
        self,
        request: RecommendationRequest
        ) -> RecommendationResponse:
        """
        Generate recommendations using Gemini.
        """

        
        if request is None:
            raise ValueError(
                "RecommendationRequest cannot be None."
            )

        if not request.insights.strip():
            raise ValueError(
                "insights cannot be empty."
            )

        prompt: str = self._build_recommendation_prompt(
            domain=request.domain,
            insights=request.insights
        )

        try:
            recommendations: str = (
                gemini_service.generate_text(
                    prompt=prompt
                )
            )

            return RecommendationResponse(
                domain=request.domain,
                recommendations=recommendations,
                model_used=GeminiService.DEFAULT_MODEL
            )

        except Exception as e:
            raise Exception(
                f"Failed to generate recommendations: {str(e)}"
            ) from e
    
