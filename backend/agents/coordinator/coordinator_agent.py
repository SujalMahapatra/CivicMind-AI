"""
CivicMind AI - Coordinator Agent

The Coordinator Agent is the entrypoint to the CivicMind AI multi-agent system.
It acts as an intelligent classifier that analyses user queries and routes them
to the most appropriate specialized agent for processing.

RULE-BASED CLASSIFICATION:
This implementation uses keyword matching for classification. Future versions
may incorporate machine learning models (e.g., BERT-based classifiers) for
improved accuracy with natural language queries.
"""

import re

from requests import request  

from .schemas import(
    Domain, Intent, RouteRequest, RouteResponse
)



class CoordinatorAgent:
    """
    Coordinator Agent for the CivicMind AI Multi-Agent System.
    
    The Coordinator Agent is the central router that receives all user queries
    and determines which specialized agent should handle each request. It
    classifies queries by:
    
    1. DOMAIN: The subject area (health, environment, mobility)
    2. INTENT: What the user wants to achieve (analytics, prediction, etc.)
    
    Responsibilities:
        - Parse incoming user queries
        - Classify queries into domains and intents using keyword matching
        - Route queries to appropriate specialized agents
        - Provide confidence scores for routing decisions
    
    Example:
        >>> agent = CoordinatorAgent()
        >>> request = RouteRequest(query="What is the air quality forecast?")
        >>> response = agent.route(request)
        >>> print(response.domain)  # Domain.environment
        >>> print(response.target_agent)  # "prediction_agent"
    
    Architecture Diagram:
        User Query -> Coordinator Agent -> RouteResponse -> Target Agent
                                |
                        +-------+-------+
                        |               |
                  detect_domain()  detect_intent()
    """
    
    # =============================================================================
    # DOMAIN KEYWORD MAPPINGS
    # =============================================================================
    # Keywords are used for rule-based classification. If query contains any
    # keyword for a domain, that domain is considered a match.
    
    DOMAIN_KEYWORDS: dict[Domain, list[str]] = {
        Domain.environment: [
            "pollution",
            "air quality",
            "emissions",
            "carbon",
            "waste",
            "recycling",
            "climate",
            "temperature",
            "environment",
            "sustainability",
            "eco",
            "green",
            "water",
            "land use",
            "biodiversity",
        ],
        Domain.health: [
            "disease",
            "illness",
            "hospital",
            "clinic",
            "patient",
            "doctor",
            "healthcare",
            "health",
            "wellness",
            "medical",
            "epidemic",
            "vaccine",
            "mental health",
        ],
        Domain.mobility: [
            "transport",
            "transportation",
            "traffic",
            "congestion",
            "road",
            "highway",
            "vehicle",
            "car",
            "bus",
            "mobility",
            "transit",
            "commute",
            "parking",
            "public transport",
        ],
    }
    
    # =============================================================================
    # INTENT KEYWORD MAPPINGS
    # =============================================================================
    # Intent keywords help determine what the user wants to accomplish.
    
    INTENT_KEYWORDS: dict[Intent, list[str]] = {
        Intent.prediction: [
            "predict",
            "forecast",
            "future",
            "projection",
            "estimate",
            "trend",
            "will be",
            "going to",
            "forecasting",
        ],
        Intent.analytics: [
            "analyze",
            "analysis",
            "analytics",
            "trend",
            "statistics",
            "patterns",
            "compare",
            "current",
            "historical",
            "past",
            "today",
        ],
        Intent.recommendation: [
            "recommend",
            "suggest",
            "improve",
            "optimize",
            "solution",
            "better",
            "should",
            "how can",
            "what should",
        ],
        Intent.report: [
            "report",
            "summary",
            "overview",
            "brief",
            "document",
            "performance",
            "monthly",
            "annual",
        ],
        Intent.knowledge: [
            "what is",
            "what are",
            "explain",
            "describe",
            "define",
            "how does",
            "why",
            "guideline",
            "policy",
            "regulation",
        ],
    }
    
    # =============================================================================
    # AGENT MAPPINGS
    # =============================================================================
    # Maps domain + intent combinations to specific agent names.
    # This enables sophisticated routing based on both dimensions.
    
    AGENT_MAP: dict[tuple[Domain, Intent], str] = {
    # Analytics
    (Domain.health, Intent.analytics): "analytics_agent",
    (Domain.environment, Intent.analytics): "analytics_agent",
    (Domain.mobility, Intent.analytics): "analytics_agent",

    # Prediction
    (Domain.health, Intent.prediction): "prediction_agent",
    (Domain.environment, Intent.prediction): "prediction_agent",
    (Domain.mobility, Intent.prediction): "prediction_agent",

    # Recommendation
    (Domain.health, Intent.recommendation): "recommendation_agent",
    (Domain.environment, Intent.recommendation): "recommendation_agent",
    (Domain.mobility, Intent.recommendation): "recommendation_agent",

    # Reports
    (Domain.health, Intent.report): "report_agent",
    (Domain.environment, Intent.report): "report_agent",
    (Domain.mobility, Intent.report): "report_agent",

    # Knowledge / RAG
    (Domain.health, Intent.knowledge): "rag_agent",
    (Domain.environment, Intent.knowledge): "rag_agent",
    (Domain.mobility, Intent.knowledge): "rag_agent",
}
    def __init__(self) -> None:
        """
        Initialize the Coordinator Agent.
        
        Creates keyword matching patterns for efficient classification.
        Patterns are pre-compiled for performance.
        """
        # Pre-compile regex patterns for domain matching (case-insensitive)
        self.domain_patterns: dict[Domain, list[re.Pattern[str]]] = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            # Each keyword becomes its own pattern for flexible matching
            self.domain_patterns[domain] = [
                re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
                for keyword in keywords
            ]
        
        # Pre-compile regex patterns for intent matching
        self.intent_patterns: dict[Intent, list[re.Pattern[str]]] = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            self.intent_patterns[intent] = [
                re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
                for keyword in keywords
            ]

    def get_domain_matches(self, query: str) -> list[str]:
        """
        Return all matched domain keywords found in the query.

        Args:
            query: User query

        Returns:
            List of matched domain keywords
        """
        query_lower = query.lower()
        matches: list[str] = []

        for keywords in self.DOMAIN_KEYWORDS.values():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    matches.append(keyword)

        return list(set(matches))
    
    def get_intent_matches(self, query: str) -> list[str]:
        """
        Return all matched intent keywords found in the query.

        Args:
            query: User query

        Returns:
            List of matched intent keywords
        """
        query_lower = query.lower()
        matches: list[str] = []

        for keywords in self.INTENT_KEYWORDS.values():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    matches.append(keyword)

        return list(set(matches))
        
    def detect_domain(self, query: str) -> tuple[Domain, float]:
        """
        Detect the domain of a query using keyword matching.
        
        Analyzes the query text to determine which domain (health, environment,
        or mobility) it relates to based on keyword presence.
        
        Args:
            query: The natural language query from the user
            
        Returns:
            tuple containing:
                - Domain: The detected domain (or Domain.unknown)
                - float: Confidence score (0.0 to 1.0)
                
        Example:
            >>> agent = CoordinatorAgent()
            >>> domain, confidence = agent.detect_domain("What is the air quality?")
            >>> print(domain)  # Domain.environment
            >>> print(confidence)  # 0.7
            
        Algorithm:
            1. Count keyword matches for each domain
            2. Calculate relative frequency across all domains
            3. Return domain with highest match count + confidence
        """
        query_lower = query.lower()
        domain_scores: dict[Domain, int] = {domain: 0 for domain in Domain}
        
        # Count matches for each domain
        for domain, patterns in self.domain_patterns.items():
            for pattern in patterns:
                if pattern.search(query_lower):
                    domain_scores[domain] += 1
        
        # Find domain with highest score
        best_domain = Domain.unknown
        best_score = 0
        total_matches = sum(domain_scores.values())
        
        for domain, score in domain_scores.items():
            if domain != Domain.unknown and score > best_score:
                best_domain = domain
                best_score = score
        
        # Calculate confidence
        if total_matches == 0:
            confidence = 0.0
        elif best_domain == Domain.unknown:
            confidence = 0.0
        else:
            confidence = best_score / total_matches
            
        return best_domain, min(confidence, 1.0)
    
    def detect_intent(self, query: str) -> tuple[Intent, float]:
        """
        Detect the intent of a query using keyword matching.
        
        Analyzes the query text to determine what the user wants to
        accomplish (prediction, analytics, recommendation, etc.).
        
        Args:
            query: The natural language query from the user
            
        Returns:
            tuple containing:
                - Intent: The detected intent (or Intent.unknown)
                - float: Confidence score (0.0 to 1.0)
                
        Example:
            >>> agent = CoordinatorAgent()
            >>> intent, confidence = agent.detect_intent("Predict traffic tomorrow")
            >>> print(intent)  # Intent.prediction
            >>> print(confidence)  # 0.5
            
        Algorithm:
            1. Count keyword matches for each intent
            2. Calculate relative frequency across all intents
            3. Return intent with highest match count + confidence
        """
        query_lower = query.lower()
        intent_scores: dict[Intent, int] = {intent: 0 for intent in Intent}
        
        # Count matches for each intent
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.search(query_lower):
                    intent_scores[intent] += 1
        
        # Find intent with highest score
        best_intent = Intent.unknown
        best_score = 0
        total_matches = sum(intent_scores.values())
        
        for intent, score in intent_scores.items():
            if intent != Intent.unknown and score > best_score:
                best_intent = intent
                best_score = score
        
        # Calculate confidence
        if total_matches == 0:
            confidence = 0.0
        elif best_intent == Intent.unknown:
            confidence = 0.0
        else:
            confidence = best_score / total_matches
            
        return best_intent, min(confidence, 1.0)
    
    
    
    def route(self, request: RouteRequest) -> RouteResponse:
        """
        Route a user query to the appropriate specialized agent.
        
        This is the main entrypoint for query processing. It:
        1. Detects the domain of the query
        2. Detects the intent of the query
        3. Determines which agent should handle the request
        4. Returns a RouteResponse with routing decision and confidence
        
        Args:
            request: The RouteRequest containing the user's query
            
        Returns:
            RouteResponse containing:
                - domain: Detected domain
                - intent: Detected intent
                - target_agent: Name of agent to handle request
                - confidence: Overall routing confidence
                
        Example:
            >>> agent = CoordinatorAgent()
            >>> request = RouteRequest(query="Predict air pollution levels")
            >>> response = agent.route(request)
            >>> print(response.target_agent)  # "environment_prediction_agent"
            >>> print(response.confidence)  # 0.8
            
        Fallback Strategy:
            - Domain unknown: Returns "coordinator_agent"
            - Intent unknown: Defaults to Intent.analytics
        """
        # Detect domain and intent
        domain, domain_confidence = self.detect_domain(request.query)
        intent, intent_confidence = self.detect_intent(request.query)
        
        #Get domain and intent matches
        domain_matches = self.get_domain_matches(request.query)
        intent_matches = self.get_intent_matches(request.query)
        
        # Handle unknown intent with fallback to analytics
        if intent == Intent.unknown:
            intent = Intent.analytics
            intent_confidence = 0.3  # Low confidence since we defaulted
            
        # Determine target agent
        if domain == Domain.unknown:
            # No domain match, use general agent with low confidence
            target_agent = "coordinator_agent"
            overall_confidence = 0.1
        else:
            # Look up agent from mapping
            agent_key = (domain, intent)
            target_agent = self.AGENT_MAP.get(agent_key, "coordinator_agent")
            
            # Combine domain and intent confidence
            # Lower confidence if either detection was weak
            overall_confidence = (domain_confidence + intent_confidence) / 2

        if domain_matches or intent_matches:
            routing_reason = (
                f"Matched domain keywords: "
                f"{', '.join(domain_matches) if domain_matches else 'None'} | "
                f"Matched intent keywords: "
                f"{', '.join(intent_matches) if intent_matches else 'None'}"
            )
        else:
            routing_reason = (
                "No keyword matches found. Routed using fallback logic."
            )
        
        return RouteResponse(
            domain=domain,
            intent=intent,
            target_agent=target_agent,
            confidence=round(min(overall_confidence, 1.0), 2),
            routing_reason = routing_reason
        )