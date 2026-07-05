"""
CivicMind AI - Recommendation Agent

This module provides the Recommendation Agent implementation for the CivicMind AI
platform. The Recommendation Agent transforms AI-generated insights into
actionable, prioritized recommendations for community stakeholders.

PURPOSE:
--------
The Recommendation Agent serves as the final step in the CivicMind AI pipeline.
While the Insight Agent interprets data and identifies patterns, the
Recommendation Agent answers: "What should we DO about this?"

The agent takes structured insights and produces concrete, actionable
guidance organized by urgency and timeframe.

MULTI-TIER RECOMMENDATIONS:
--------------------------
The agent generates three tiers of recommendations:

1. IMMEDIATE ACTIONS (Crisis Response):
   - Actions to take within hours/days
   - Emergency interventions
   - Quick wins with immediate impact
   
2. PREVENTIVE ACTIONS (Risk Mitigation):
   - Actions to prevent problems from worsening
   - Medium-term initiatives (weeks/months)
   - Proactive measures
   
3. LONG-TERM STRATEGIC ACTIONS:
   - Sustainable, systemic changes
   - Policy and infrastructure initiatives
   - Multi-year strategic investments

ARCHITECTURE IN THE PIPELINE:
-----------------------------
The Recommendation Agent is positioned at the end of the agent chain:

    Coordinator Agent
           ↓
    Analytics Agent → Data & Statistics
           ↓
    Prediction Agent → Forecasts & Trends  \
           ↓                                ↘
    Insight Agent → Findings & Risks → Recommendation Agent → Actions
           ↑                                ↗
    [Domain Context: health/environment/mobility]

CLEAN ARCHITECTURE:
-------------------
- Single Responsibility: Only generates recommendations from insights
- Dependency Inversion: Uses GeminiService interface, not SDK directly
- Separation of Concerns: Prompt building separate from API calls
- DRY: Reuses GeminiService instead of duplicating AI integration

PROMPT ENGINEERING:
------------------
WHY THIS PROMPT STRUCTURE:
    - Three-tier output forces actionable (not observational) responses
    - Domain context ensures recommendations fit the subject area
    - Urgency levels help stakeholders prioritize resources
    - Constraints prevent generic advice
"""

import re
from typing import Optional

from schemas import Domain, RecommendationRequest, RecommendationResponse


class RecommendationAgent:
    """
    Recommendation Agent for CivicMind AI Multi-Agent System.
    
    The Recommendation Agent converts AI-generated insights into actionable,
    prioritized recommendations for communities, organizations, and stakeholders.
    It serves as the bridge between data interpretation and decision-making.
    
    Key Responsibilities:
        - Transform insights into concrete action items
        - Organize recommendations by urgency/immediacy
        - Ensure recommendations are domain-appropriate
        - Generate actionable output for end-users
    
    Key Distinctions:
    ----------------
    VS Insight Agent:
        - Insight Agent: Identifies what the data shows ("Air quality is declining")
        - Recommendation Agent: Advises what to do about it ("Issue air quality alerts")
        
    VS Prediction Agent:
        - Prediction Agent: Forecasts future states ("AQI will reach 120")
        - Recommendation Agent: Determines responses ("Prepare emergency protocols")
    
    Example Usage:
        >>> from services.gemini_service import GeminiService
        >>> gemini_service = GeminiService()
        >>> 
        >>> agent = RecommendationAgent(gemini_service)
        >>> request = RecommendationRequest(
        ...     domain=Domain.environment,
        ...     insights="Air quality declining. AQI forecast to reach 120."
        ... )
        >>> recommendations = agent.generate_recommendations(request)
        >>> print(recommendations.immediate_actions)
        "1. Issue air quality alerts..."
        >>> print(recommendations.long_term_actions)
        "1. Transition to electric infrastructure..."
    """
    
    def __init__(self, gemini_service) -> None:
        """
        Initialize the Recommendation Agent with Gemini service.
        
        Args:
            gemini_service: Configured GeminiService instance
        """
        if gemini_service is None:
            raise ValueError("gemini_service is required")
        
        self.gemini_service = gemini_service
    
    def _build_recommendation_prompt(
        self,
        domain: Domain,
        insights: str
    ) -> str:
        """
        Build a structured prompt for generating recommendations.
        
        Args:
            domain: Subject domain
            insights: AI-generated insights
            
        Returns:
            str: Formatted prompt
        """
        domain_descriptions: dict[Domain, str] = {
            Domain.health: "public health and healthcare",
            Domain.environment: "environmental sustainability",
            Domain.mobility: "urban mobility and transportation",
            Domain.unknown: "community services"
        }
        
        domain_context: str = domain_descriptions.get(domain, "community services")
        
        prompt: str = f"""You are a community advisory specialist for {domain_context}.

Your task is to convert the following insights into specific, actionable recommendations for community stakeholders.

INSIGHTS TO ACT ON:
{insights}

Generate recommendations in THREE categories:

1. IMMEDIATE ACTIONS (Hours/Days):
What should decision-makers do RIGHT NOW? Include 2-4 specific, concrete actions.
- Focus on crisis response or quick wins
- Be specific: who should do what

2. PREVENTIVE ACTIONS (Weeks/Months):
What preventive measures should be implemented?
- How to stop problems from getting worse
- Proactive policy or operational changes

3. LONG-TERM STRATEGIC ACTIONS (Years):
What sustainable, systemic changes should be pursued?
- Infrastructure investments
- Policy reforms
- Long-term strategic initiatives

Format each action as a numbered list. Be specific and actionable. Avoid vague advice like "monitor the situation" or "be aware of." Each recommendation should be implementable."""
        
        return prompt
    
    def _parse_recommendations(
        self,
        raw_response: str,
        model_used: str
    ) -> RecommendationResponse:
        """
        Parse raw Gemini response into structured RecommendationResponse.
        
        Args:
            raw_response: Raw text from Gemini
            model_used: Model name
            
        Returns:
            RecommendationResponse with three action categories
        """
        import re
        
        # Initialize with empty/default content
        immediate_actions: str = ""
        preventive_actions: str = ""
        long_term_actions: str = ""
        
        # Try to extract numbered sections
        patterns: list[tuple[str, str]] = [
            (r"1\.\\s*(?:IMMEDIATE)?(?:.*?)?ACTIONS:?(.*?)(?=2\\.|$)", "immediate"),
            (r"2\.\\s*(?:PREVENTIVE)?(?:.*?)?ACTIONS:?(.*?)(?=3\\.|$)", "preventive"),
            (r"3\.\\s*(?:LONG[- ]?TERM)?(?:.*?)?ACTIONS:?(.*?)(?=4\\.|$)", "long_term"),
            (r"3\.\\s*(?:LONG[- ]?TERM)?(?:.*?)?STRATEGIC?:?(.*?)(?=$)", "long_term"),
        ]
        
        for pattern, section_key in patterns:
            match = re.search(pattern, raw_response, re.IGNORECASE | re.DOTALL)
            if match:
                content: str = match.group(1).strip()
                if section_key == "immediate":
                    immediate_actions = content
                elif section_key == "preventive":
                    preventive_actions = content
                elif section_key == "long_term":
                    long_term_actions = content
        
        # Fallback: Use entire response
        if not immediate_actions:
            lines: list[str] = raw_response.split('\\n')
            immediate_actions = "\\n".join(lines[:10]) or raw_response
            preventive_actions = "N/A"
            long_term_actions = "N/A"
        
        # Ensure sections are not empty
        immediate_actions = immediate_actions or "No immediate actions specified."
        preventive_actions = preventive_actions or "No preventive actions specified."
        long_term_actions = long_term_actions or "No long-term actions specified."
        
        return RecommendationResponse(
            immediate_actions=immediate_actions,
            preventive_actions=preventive_actions,
            long_term_actions=long_term_actions,
            model_used=model_used
        )
    
    def generate_recommendations(
        self,
        request: RecommendationRequest
    ) -> RecommendationResponse:
        """
        Generate actionable recommendations from insights.
        
        Args:
            request: RecommendationRequest with domain and insights
            
        Returns:
            RecommendationResponse with three recommendation categories
            
        Raises:
            ValueError: If request is invalid
            Exception: If Gemini API fails
        """
        # VALIDATION
        if request is None:
            raise ValueError("RecommendationRequest cannot be None")
        
        if not request.insights or len(request.insights.strip()) == 0:
            raise ValueError("insights is required")
        
        # BUILD PROMPT
        prompt: str = self._build_recommendation_prompt(
            domain=request.domain,
            insights=request.insights
        )
        
        # CALL SERVICE
        try:
            raw_response: str = self.gemini_service.generate_text(prompt)
        except Exception as e:
            raise Exception(f"Failed to generate recommendations: {str(e)}") from e
        
        # VALIDATE RESPONSE
        if not raw_response or len(raw_response.strip()) == 0:
            raise ValueError("Empty response from Gemini")
        
        # IMPORT MODEL NAME
        from services.gemini_service import GeminiService
        
        # PARSE RESPONSE
        recommendations: RecommendationResponse = self._parse_recommendations(
            raw_response=raw_response,
            model_used=GeminiService.DEFAULT_MODEL
        )
        
        return recommendations
