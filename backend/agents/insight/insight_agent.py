"""
CivicMind AI - Insight Agent

This module provides the Insight Agent implementation for the CivicMind AI
platform. The Insight Agent transforms raw analytics and predictions into
actionable decision intelligence using Google's Gemini AI.

PURPOSE:
--------
While Analytics Agents process data and Prediction Agents forecast trends,
the Insight Agent bridges the gap between raw data and human understanding.
It answers: "What does this data mean for decision-makers?"

The Insight Agent synthesizes:
- Statistical outputs from Analytics Agent
- Forecast results from Prediction Agent  
- Domain context (health, environment, mobility)

And produces:
- Human-readable insights
- Identified risks and concerns
- Trend explanations
- Community impact assessments

ARCHITECTURE ROLE:
------------------
The Insight Agent sits between data processing (Analytics) and
decision-making (Recommendations) in the agent pipeline:

    User Query -> Coordinator -> Analytics Agent -> Insight Agent
                                     |                  
                                     v                  
                              Prediction Agent           
                                     |                  
                                     v                  
                            Recommendation Agent -> Output

CLEAN ARCHITECTURE:
-------------------
- Single Responsibility: Only generates insights, no analytics computation
- Dependency Inversion: Depends on GeminiService interface, not SDK directly
- Separation of Concerns: Prompt building is separate from API calls
- DRY: Reuses GeminiService instead of duplicating AI integration code

PROMPT ENGINEERING:
------------------
WHY PROMPT ENGINEERING MATTERS:
    The prompt is the primary interface between the application and the AI.
    A well-crafted prompt:
    - Directs the AI to focus on relevant aspects
    - Ensures consistent output structure
    - Reduces hallucination by grounding in provided data
    - Increases response quality through context setting
"""

import re
from typing import Optional

from schemas import Domain, InsightRequest, InsightResponse


class InsightAgent:
    """
    Insight Agent for CivicMind AI Multi-Agent System.
    
    The Insight Agent converts structured analytics and prediction outputs
    into human-readable decision intelligence. It leverages Gemini AI to
    synthesize raw statistics into actionable insights.
    
    Key Distinctions:
    ----------------
    VS Analytics Agent:
        - Analytics Agent: Computes raw statistics (rows, averages, counts)
        - Insight Agent: Interprets those statistics into meaning
        
    VS Prediction Agent:
        - Prediction Agent: Generates numerical forecasts and probabilities
        - Insight Agent: Explains what those forecasts imply for decisions
    
    Example Usage:
        >>> # Assuming gemini_service is initialized elsewhere
        >>> agent = InsightAgent(gemini_service)
        >>> request = InsightRequest(
        ...     domain=Domain.environment,
        ...     analytics_summary="Air quality index: AQI 45",
        ...     prediction_summary="AQI expected to rise to 80"
        ... )
        >>> insights = agent.generate_insights(request)
    """
    
    def __init__(self, gemini_service) -> None:
        """
        Initialize the Insight Agent with Gemini service dependency.
        
        The Insight Agent requires a GeminiService instance to generate
        AI-powered insights. This dependency injection pattern allows:
        - Reuse of existing service instances
        - Easy testing with mock services
        - Flexible configuration
        
        Args:
            gemini_service: Configured GeminiService instance
            
        Raises:
            ValueError: If gemini_service is None
        """
        if gemini_service is None:
            raise ValueError(
                "gemini_service is required. "
                "Please provide a configured GeminiService instance."
            )
        
        self.gemini_service = gemini_service
    
    def _build_insight_prompt(
        self,
        domain: Domain,
        analytics_summary: str,
        prediction_summary: str
    ) -> str:
        """
        Build a high-quality prompt for insight generation.
        
        This method constructs a structured prompt that guides Gemini to focus
        on relevant domain context and synthesize the analytics and predictions
        into actionable insights.
        
        WHY THIS PROMPT STRUCTURE:
            - Role assignment establishes expertise expectations
            - Context sections ground the AI in specific data
            - Explicit output format ensures consistent structure
            - Constraints prevent hallucination beyond provided data
        
        Args:
            domain: The subject domain (health, environment, mobility)
            analytics_summary: Statistical results in text format
            prediction_summary: Forecast results in text format
            
        Returns:
            str: Complete formatted prompt ready for Gemini API
        """
        # Map domain to human-readable description
        domain_descriptions: dict[Domain, str] = {
            Domain.health: "public health and healthcare services",
            Domain.environment: "environmental sustainability and air quality",
            Domain.mobility: "urban mobility and transportation systems",
            Domain.unknown: "community services and infrastructure"
        }
        
        domain_context: str = domain_descriptions.get(domain, "community services")
        
        # Build the structured prompt
        prompt: str = f"""You are a community decision intelligence analyst specializing in {domain_context}.

Your task is to analyze the provided analytics data and predictions, then generate actionable insights for community stakeholders.

ANALYTICS DATA:
{analytics_summary}

PREDICTION DATA:
{prediction_summary}

Based ONLY on the data above, generate insights organized into these four sections:

1. KEY FINDINGS:
Extract the most important 2-3 findings from the analytics. What do the numbers actually show?

2. EMERGING RISKS:
Identify 1-2 potential risks or concerns based on the predictions and current state.

3. IMPORTANT TRENDS:
Describe 1-2 meaningful patterns or trends evident in the data.

4. COMMUNITY IMPACT:
Explain how these findings affect the community in plain language decision-makers can understand.

Format each section clearly with headers. Be specific and cite data where relevant. Keep the total response concise (300-500 words)."""
        
        return prompt
    
    def _parse_insights_response(
        self,
        raw_response: str,
        model_used: str
    ) -> InsightResponse:
        """
        Parse raw Gemini response into structured InsightResponse.
        
        Gemini returns insights as a single text block with headers.
        This method extracts the four sections and maps them to the
        structured response model.
        
        Args:
            raw_response: Raw text from Gemini API
            model_used: Name of Gemini model used
            
        Returns:
            InsightResponse: Structured insights with four sections
        """
        # Initialize with empty content
        key_findings: str = ""
        emerging_risks: str = ""
        important_trends: str = ""
        community_impact: str = ""
        
        # Parse by looking for numbered sections
        patterns: list[tuple[str, str]] = [
            (r"1\.\\s*(?:KEY)?\\s*FINDINGS:?(.*?)(?=2\\.|$)", "key_findings"),
            (r"2\.\\s*(?:EMERGING)?\\s*RISKS:?(.*?)(?=3\\.|$)", "emerging_risks"),
            (r"3\.\\s*(?:IMPORTANT)?\\s*TRENDS:?(.*?)(?=4\\.|$)", "important_trends"),
            (r"4\.\\s*(?:COMMUNITY)?\\s*IMPACT:?(.*?)(?=$)", "community_impact"),
        ]
        
        for pattern, section_key in patterns:
            match = re.search(pattern, raw_response, re.IGNORECASE | re.DOTALL)
            if match:
                content: str = match.group(1).strip()
                if section_key == "key_findings":
                    key_findings = content
                elif section_key == "emerging_risks":
                    emerging_risks = content
                elif section_key == "important_trends":
                    important_trends = content
                elif section_key == "community_impact":
                    community_impact = content
        
        # Fallback: If parsing failed, use entire response
        if not key_findings and not emerging_risks:
            key_findings = raw_response
            emerging_risks = "N/A"
            important_trends = "N/A"
            community_impact = "N/A"
        
        # Ensure no section is empty
        key_findings = key_findings or "No specific findings extracted."
        emerging_risks = emerging_risks or "No specific risks identified."
        important_trends = important_trends or "No specific trends identified."
        community_impact = community_impact or "See key findings for impact."
        
        return InsightResponse(
            key_findings=key_findings,
            emerging_risks=emerging_risks,
            important_trends=important_trends,
            community_impact=community_impact,
            model_used=model_used
        )
    
    def generate_insights(self, request: InsightRequest) -> InsightResponse:
        """
        Generate actionable insights from analytics and prediction summaries.
        
        This is the main entrypoint for the Insight Agent. It builds a
        structured prompt with domain context, calls Gemini AI via the
        service layer, and parses the response into structured sections.
        
        Args:
            request: InsightRequest containing domain, analytics_summary,
                    and prediction_summary
                
        Returns:
            InsightResponse with key_findings, emerging_risks,
            important_trends, community_impact, and model_used
            
        Raises:
            ValueError: If request is invalid or missing required fields
            Exception: If Gemini API call fails
            
        Example:
            >>> request = InsightRequest(
            ...     domain=Domain.health,
            ...     analytics_summary="15 hospitals, 1200 daily visits",
            ...     prediction_summary="Visits increasing 5% monthly"
            ... )
            >>> insights = agent.generate_insights(request)
            >>> print(insights.key_findings)
        """
        # VALIDATION: Ensure request is valid
        if request is None:
            raise ValueError("InsightRequest cannot be None")
        
        if not request.analytics_summary or len(request.analytics_summary.strip()) == 0:
            raise ValueError("analytics_summary is required and cannot be empty")
        
        if not request.prediction_summary or len(request.prediction_summary.strip()) == 0:
            raise ValueError("prediction_summary is required and cannot be empty")
        
        # STEP 1: Build the structured prompt
        prompt: str = self._build_insight_prompt(
            domain=request.domain,
            analytics_summary=request.analytics_summary,
            prediction_summary=request.prediction_summary
        )
        
        # STEP 2: Call Gemini via the service layer
        try:
            raw_response: str = self.gemini_service.generate_text(prompt)
        except Exception as e:
            raise Exception(
                f"Failed to generate insights using Gemini API. "
                f"Error: {str(e)}"
            ) from e
        
        # VALIDATION: Ensure we got a response
        if not raw_response or len(raw_response.strip()) == 0:
            raise ValueError(
                "Gemini returned an empty response. Unable to generate insights."
            )
        
        # STEP 3: Parse the response into structured sections
        # Import GeminiService to get DEFAULT_MODEL
        from services.gemini_service import GeminiService
        
        insights: InsightResponse = self._parse_insights_response(
            raw_response=raw_response,
            model_used=GeminiService.DEFAULT_MODEL
        )
        
        return insights
