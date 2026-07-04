"""
CivicMind AI - Pydantic Schemas

This module defines Pydantic models for the Coordinator Agent data structures.
Pydantic is Python's most widely-used data validation library that uses type hints
to define schemas, perform validation, and enable JSON serialization.

PYDANTIC V2 SYNTAX:
This file uses Pydantic V2 syntax, which differs from V1 in several ways:
- model_config is a ConfigDict or class attribute
- Field types use Pydantic's Field() function instead of FieldInfo
- Validation is separate from schema generation
- Use model_validator and field_validator instead of root_validator/validator
"""

from enum import Enum


from pydantic import BaseModel, Field, ConfigDict


# =============================================================================
# ENUMERATIONS
# =============================================================================
# Enums (enumerations) define a fixed set of named values. Using enums instead
# of plain strings ensures type safety, allows IDE autocomplete, and prevents
# invalid values from being passed.


class Domain(str,Enum):
    """
    Domain categories for CivicMind AI queries.
    
    CivicMind AI categorizes all user queries into domains to route them
    to specialized agents with relevant expertise.
    
    Attributes:
        health: Public health and wellness topics (hospitals, disease tracking)
        environment: Sustainability and eco topics (air quality, pollution)
        mobility: Transportation and urban planning (traffic, infrastructure)
        unknown: When classification cannot determine domain
    """
    health = "health"
    environment = "environment"
    mobility = "mobility"
    unknown = "unknown"


class Intent(str,Enum):
    """
    User intent categories for CivicMind AI queries.
    
    Intent classification determines what the user wants to achieve - whether
    they want data analysis, forecasting, or specific recommendations.
    
    Attributes:
        analytics: Analyze current/past data for insights
        prediction: Forecast future trends and outcomes
        recommendation: Get actionable suggestions
        report: Generate comprehensive documents
        knowledge: Learn about a topic (RAG-based answers)
        unknown: When intent cannot be determined
    """
    analytics = "analytics"
    prediction = "prediction"
    recommendation = "recommendation"
    report = "report"
    knowledge = "knowledge"
    unknown = "unknown"


# =============================================================================
# PYDANTIC MODELS
# =============================================================================
# Pydantic BaseModel is the core class for creating data schemas. It provides:
# - Automatic JSON serialization/deserialization
# - Type validation before assignment
# - Clear error messages when validation fails
# - IDE support through type hints


class RouteRequest(BaseModel):
    """
    Request model for routing a user query to the appropriate agent.
    
    This model captures the raw user input that needs to be analyzed
    and routed to specialized agents based on domain and intent.
    
    Attributes:
        query: The natural language query from the user
        
    Example:
        >>> route_request = RouteRequest(query="What is the air quality forecast?")
        >>> print(route_request.query)
        "What is the air quality forecast?"
        
    Validation:
        - query: Must be non-empty string, max 10000 chars
    """
    
    # The user's natural language query
    # Using Field() allows us to add metadata, validation constraints, and descriptions
    query: str = Field(
        ...,  # Ellipsis means this field is required
        min_length=1,
        max_length=10000,
        description="Natural language query to be routed to appropriate agent",
        examples=["What is the air quality forecast for tomorrow?"]
    )
    
    # Pydantic V2: Use model_config for additional configuration
    # strip_whitespace removes leading/trailing whitespace during validation
    model_config: ConfigDict = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "query": "What is the air quality forecast for tomorrow?"
            }
        }
    )


class RouteResponse(BaseModel):
    """
    Response model containing routing decision from Coordinator Agent.
    
    After the Coordinator Agent analyzes the user's query, this model
    represents the routing decision indicating which specialized agent
    should handle the request.
    
    Attributes:
        domain: The domain category of the query
        intent: The user's intent/what they want to achieve
        target_agent: Name of the agent selected to handle this request
        confidence: Confidence score (0.0 to 1.0) for the routing decision
        
    Example:
        >>> response = RouteResponse(
        ...     domain=Domain.environment,
        ...     intent=Intent.prediction,
        ...     target_agent="prediction_agent",
        ...     confidence=0.95
        ... )
        
    Validation:
        - confidence: Must be between 0.0 and 1.0
    """
    
    # Domain classification: health, environment, mobility, or unknown
    domain: Domain = Field(
        ...,  # Required field
        description="Classified domain for the query",
        examples=[Domain.environment]
    )
    
    # Intent classification: what the user wants to do
    intent: Intent = Field(
        ...,  # Required field
        description="Classified intent for the query",
        examples=[Intent.prediction]
    )
    
    # Target agent name (e.g., "analytics_agent", "prediction_agent")
    target_agent: str = Field(
        ...,  # Required field
        min_length=1,
        max_length=100,
        description="Name of the agent selected to handle this request",
        examples=["prediction_agent"]
    )
    
    # Confidence score (0.0 to 1.0) of the routing decision
    # Higher values indicate more confident classification
    confidence: float = Field(
        ...,  # Required field
        ge=0.0,  # Greater than or equal to 0.0
        le=1.0,  # Less than or equal to 1.0
        description="Confidence score (0.0 to 1.0) of the routing decision",
        examples=[0.95]
    )
    routing_reason: str = Field(
    ...,
    min_length=1,
    description="Explanation of why the query was routed to the selected agent"
    )
    # Pydantic V2: Configuration for this model
    model_config: ConfigDict = ConfigDict(
        # Enable serialization of enum values directly
        use_enum_values=True,
        # Allow population by name (e.g., domain="health")
        populate_by_name=True,
        # JSON example for documentation
        json_schema_extra={
            "example": {
                "domain": "environment",
                "intent": "prediction",
                "target_agent": "prediction_agent",
                "confidence": 0.95,
                "routing_reason": "Matched keywords: traffic, congestion, predict"
            }
        }
    )
