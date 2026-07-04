"""
CivicMind AI - Coordinator Router

This module provides the HTTP endpoints for the Coordinator Agent.
The Coordinator Agent acts as the entrypoint to the multi-agent system,
receiving user queries and routing them to specialized agents.

ENDPOINT DOCUMENTATION:
    POST /coordinator/route
        - Receives user queries
        - Returns routing decision with domain, intent, and target agent
        - Uses CoordinatorAgent for classification logic

DESIGN PATTERNS:
    - Dependency Injection: CoordinatorAgent is instantiated once at module load
    - Separation of Concerns: Router handles HTTP, CoordinatorAgent handles logic
    - Pydantic Validation: Request/Response models enforce type safety

EXAMPLE USAGE:
    >>> import requests
    >>> response = requests.post(
    ...     "http://localhost:8000/coordinator/route",
    ...     json={"query": "Predict air quality tomorrow"}
    ... )
    >>> print(response.json())
    {
        "domain": "environment",
        "intent": "prediction",
        "target_agent": "environment_prediction_agent",
        "confidence": 0.9
    }
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from schemas import Domain, Intent, RouteRequest, RouteResponse
from agent import CoordinatorAgent


# =============================================================================
# ROUTER INITIALIZATION
# =============================================================================
# Create an APIRouter instance to group coordinator-related endpoints.
# The prefix '/coordinator' means all routes will be prefixed with this path.
# Tags appear in the auto-generated API documentation (Swagger UI).

router = APIRouter(
    prefix="/coordinator",
    tags=["Coordinator"],
    # responses provides default error response structure for documentation
    responses={
        404: {"description": "Coordinator endpoint not found"},
        422: {"description": "Validation error - invalid request format"},
        500: {"description": "Internal server error"},
    },
)


# =============================================================================
# COORDINATOR AGENT INSTANCE
# =============================================================================
# Instantiate the CoordinatorAgent at module level (singleton pattern).
# This ensures:
# - Single initialization: Keyword patterns are compiled once
# - Shared state: All requests use the same agent instance
# - Performance: No per-request instantiation overhead
# 
# For production, you might want to use FastAPI's dependency injection
# system with yield for database connections or external API clients.

coordinator_agent: CoordinatorAgent = CoordinatorAgent()


# =============================================================================
# ROUTE ENDPOINT
# =============================================================================

@router.post(
    "/route",
    response_model=RouteResponse,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Route a user query to the appropriate agent",
    description="""
    Receives a user query and returns routing information indicating which
    specialized agent should handle the request.
    
    The Coordinator Agent analyzes the query to determine:
    - Domain: Subject area (health, environment, mobility)
    - Intent: What the user wants (prediction, analytics, etc.)
    - Target Agent: Name of the specialized agent to handle the request
    - Confidence: How confident the router is in its decision (0.0 to 1.0)
    
    If the domain cannot be determined, the query is routed to a general
    agent with appropriate fallback handling.
    """,
    response_description="Routing decision with domain, intent, and target agent",
)
async def route_query(request: RouteRequest) -> RouteResponse:
    """
    Process a user query and return routing decision.
    
    This endpoint is the main entrypoint for the CivicMind AI system.
    It accepts natural language queries and returns structured routing
    information for downstream processing by specialized agents.
    
    Args:
        request: RouteRequest containing the user's natural language query
        
    Returns:
        RouteResponse containing:
            - domain: The classified subject area
            - intent: The detected user intent  
            - target_agent: Agent name to handle the request
            - confidence: Routing confidence score (0.0 to 1.0)
            
    Raises:
        HTTPException: If processing fails (500 error)
        
    Example Request:
        {
            "query": "Predict traffic congestion next week"
        }
        
    Example Response:
        {
            "domain": "mobility",
            "intent": "prediction",
            "target_agent": "mobility_prediction_agent",
            "confidence": 0.9
        }
        
    Domain Mapping:
        - "Predict air quality" -> environment
        - "Analyze disease trends" -> health
        - "Recommend transport solutions" -> mobility
        
    Intent Mapping:
        - "Predict tomorrow" -> prediction
        - "Analyze current data" -> analytics
        - "How can we improve?" -> recommendation
        - "Generate report" -> report
        - "What is air quality?" -> knowledge
    """
    try:
        # Process the query through the Coordinator Agent
        # The agent classifies domains/intents and selects the target agent
        route_response: RouteResponse = coordinator_agent.route(request)
        
        return route_response
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error routing query: {e}")
        
        # Return a 500 error if processing fails
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


# =============================================================================
# OPTIONAL: BATCH ROUTE ENDPOINT
# =============================================================================
# You can extend this router with batch processing for multiple queries

# from typing import List
# 
# @router.post(
#     "/route/batch",
#     response_model=List[RouteResponse],
#     summary="Process multiple queries in batch",
# )
# async def route_batch(requests: List[RouteRequest]) -> List[RouteResponse]:
#     """
#     Process multiple queries and return routing decisions for each.
#     
#     Useful for batch processing or queue-based systems that need
#     to route multiple queries efficiently.
#     """
#     responses = []
#     for request in requests:
#         response = coordinator_agent.route(request)
#         responses.append(response)
#     return responses
