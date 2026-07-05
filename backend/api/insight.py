"""
CivicMind AI - Insight Router

This module exposes HTTP endpoints for the Insight Agent.

## PURPOSE:

The Insight Agent transforms structured analytics and prediction
outputs into human-readable decision intelligence using Gemini.

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

## ENDPOINTS:

POST /insight/generate
Generate AI-powered insights from analytics and prediction summaries.
"""

from fastapi import APIRouter, HTTPException, status

from agents.insight.insight_agent import InsightAgent

from agents.insight.schemas import (
    InsightRequest,
    InsightResponse
)

# =============================================================================

# ROUTER INITIALIZATION

# =============================================================================

router = APIRouter(
prefix="/insight",
tags=["Insight"]
)

# =============================================================================

# AGENT INITIALIZATION

# =============================================================================

insight_agent = InsightAgent()

# =============================================================================

# INSIGHT GENERATION ENDPOINT

# =============================================================================

@router.post(
    "/generate",
    response_model=InsightResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI-powered insights",
    description=(
        "Generate community intelligence insights using "
        "analytics and prediction summaries."
    )
)

async def generate_insights(
    request: InsightRequest
    ) -> InsightResponse:
    """
    Generate decision-intelligence insights.


    Request Example:
    ----------------

    {
        "domain": "environment",
        "analytics_summary":
            "Dataset contains 1000 rows with quality score 95.",
        "prediction_summary":
            "AQI expected to increase from 180 to 220."
    }

    Returns:
    --------
    InsightResponse
    """

    try:
        return insight_agent.generate_insights(
            request=request
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

