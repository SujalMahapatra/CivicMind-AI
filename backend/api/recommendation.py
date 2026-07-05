"""
CivicMind AI - Recommendation Router

This module exposes HTTP endpoints for the Recommendation Agent.

## PURPOSE:

The Recommendation Agent converts AI-generated insights into
actionable recommendations for communities, organizations,
and decision-makers.

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

## ENDPOINTS:

POST /recommendation/generate
Generate actionable recommendations from insights.
"""

from fastapi import APIRouter, HTTPException, status

from agents.recommendation.recommendation_agent import (
RecommendationAgent
)

from agents.recommendation.schemas import (
RecommendationRequest,
RecommendationResponse
)

# =============================================================================

# ROUTER INITIALIZATION

# =============================================================================

router = APIRouter(
prefix="/recommendation",
tags=["Recommendation"]
)

# =============================================================================

# AGENT INITIALIZATION

# =============================================================================

recommendation_agent = RecommendationAgent()

# =============================================================================

# RECOMMENDATION ENDPOINT

# =============================================================================

@router.post(
"/generate",
response_model=RecommendationResponse,
status_code=status.HTTP_200_OK,
summary="Generate AI-powered recommendations",
description=(
"Generate actionable recommendations "
"from AI-generated insights."
)
)
async def generate_recommendations(
    request: RecommendationRequest
    ) -> RecommendationResponse:
    """
    Generate recommendations.

    ```
    Example Request:

    {
        "domain": "environment",
        "insights": "AQI is expected to increase significantly."
    }

    Returns:
        RecommendationResponse
    """

    try:
        return recommendation_agent.generate_recommendations(
            request=request
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

