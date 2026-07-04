"""
CivicMind AI - Gemini Service

This module provides a reusable service layer for integrating with Google's
Gemini API. The GeminiService acts as a centralized interface for all AI
text generation capabilities across the CivicMind AI platform.

ARCHITECTURE PATTERNS:
--------------------
WHY A SERVICE LAYER EXISTS:
    A service layer provides an abstraction between your application logic
    and external APIs. Benefits include:
    - Reusability: One implementation used by all agents
    - Testability: Easy to mock for unit testing
    - Maintainability: API changes only need updates in one place
    - Configuration: Centralized API key management and retry logic

WHY CENTRALIZE AI INTEGRATIONS:
    Centralizing the Gemini integration prevents:
    - Duplicate API key management
    - Inconsistent error handling
    - Multiple client instantiations (resource waste)
    - Scattered configuration across codebase

CLEAN ARCHITECTURE PRINCIPLES:
    - Single Responsibility: This service only handles Gemini API calls
    - Dependency Inversion: Agents depend on service interface, not SDK directly
    - Interface Segregation: Simple, focused methods (generate_text, ask_question)
    - Don't Repeat Yourself (DRY): One place for API configuration

GOOGLE GEMINI SDK:
    This module uses the newer google.genai SDK (not the legacy
    google.generativeai). The new SDK:
    - Better async support
    - Simplified client initialization
    - Improved error handling
    - Future-proof for Gemini 2.x models

Example Usage:
    >>> from services.gemini_service import GeminiService
    >>> service = GeminiService()
    >>> response = service.generate_text("Explain air pollution.")
    >>> print(response)
    "Air pollution refers to..."
"""

from typing import Optional

from google import genai
from google.genai import types

from config import settings


# =============================================================================
# CONSTANTS
# =============================================================================
# These constants define default behaviors and can be overridden per-call.

DEFAULT_MODEL: str = "gemini-2.5-flash"
"""
Default Gemini model for text generation.

Current recommendation: gemini-2.5-flash
- Fast response times
- Cost-effective for most use cases
- Excellent for summarization and Q&A

Alternative models for different needs:
- gemini-2.5-pro: Higher quality, longer context, more expensive
- gemini-2.0-flash: Legacy stable model (keep as fallback)
- Future models: Updated as Google releases new versions

USAGE:
    Pass model_name parameter to override:
    >>> service.generate_text("prompt", model_name="gemini-2.5-pro")
"""

DEFAULT_TEMPERATURE: float = 0.7
"""
Temperature controls response creativity (0.0 = deterministic, 1.0 = creative).

Guidelines:
- 0.0-0.3: Factual queries, code generation
- 0.4-0.7: Balanced responses (default)
- 0.8-1.0: Creative writing, brainstorming
"""

DEFAULT_MAX_TOKENS: int = 2048
"""
Maximum tokens (roughly words) in the response.

Token estimation:
- ~4 characters = 1 token
- Full response often needs 500-2000 tokens
"""


class GeminiServiceException(Exception):
    """
    Custom exception for Gemini service errors.
    
    Provides structured error messages for debugging and logging.
    
    Attributes:
        message: Human-readable error description
        original_error: The underlying exception (if any)
        error_code: Optional error classification
    """
    
    def __init__(
        self,
        message: str,
        original_error: Optional[Exception] = None,
        error_code: Optional[str] = None
    ) -> None:
        """Initialize exception with context."""
        super().__init__(message)
        self.message = message
        self.original_error = original_error
        self.error_code = error_code
    
    def __str__(self) -> str:
        """String representation with error context."""
        if self.original_error:
            return f"{self.message} | Original: {self.original_error}"
        return self.message


class GeminiService:
    """
    Service layer for Google Gemini API integration.
    
    The GeminiService provides a clean, reusable interface for generating
    text using Google's Gemini models. It's designed to be instantiated
    once and reused across multiple agents to avoid redundant API client
    creation and ensure consistent configuration.
    
    Key Responsibilities:
        - Manage Gemini API client lifecycle
        - Handle API key configuration
        - Provide text generation interface
        - Implement error handling and retries
        - Support multiple model configurations
    
    Thread Safety:
        The Gemini client is thread-safe, so a single service instance
        can be shared across multiple threads/async tasks safely.
    
    Resource Management:
        The service maintains a persistent client connection. For optimal
        performance, create one instance and reuse it (singleton pattern).
    
    Example:
        >>> service = GeminiService()
        >>> # Reuse across agents
        >>> analytics_response = service.generate_text(
        ...     "Analyze these trends: ...",
        ...     model_name="gemini-2.5-pro"  # Use pro for complex analysis
        ... )
        >>> recommendation_response = service.generate_text(
        ...     "Recommend improvements: ..."
        ... )  # Uses default flash model
        
    Error Handling:
        >>> try:
        ...     response = service.generate_text("prompt")
        ... except GeminiServiceException as e:
        ...     print(f"Service error: {e.message}")
    """
    
    def __init__(self) -> None:
        """
        Initialize GeminiService with Google GenAI client.
        
        This constructor validates configuration and creates a reusable
        Gemini client instance. The client is stored as an instance variable
        for efficient reuse across multiple API calls.
        
        Configuration Validation:
            - GEMINI_API_KEY must be set in settings
            - Empty or missing keys raise GeminiServiceException
            
        Raises:
            GeminiServiceException: If GEMINI_API_KEY is not configured
            
        Example:
            >>> try:
            ...     service = GeminiService()
            ... except GeminiServiceException as e:
            ...     print(f"Failed to initialize: {e}")
            ...     # Handle missing API key gracefully
            
        Note:
            This performs synchronous initialization. For async contexts,
            create the service during startup or use dependency injection.
        """
        # VALIDATION: Ensure API key is configured
        # Security: Never hardcode API keys, always use environment/config
        api_key: str = settings.GEMINI_API_KEY
        
        if not api_key or len(api_key.strip()) == 0:
            raise GeminiServiceException(
                "GEMINI_API_KEY is not configured. "
                "Please set it in your .env file or environment variables.",
                error_code="MISSING_API_KEY"
            )
        
        # Initialize the Gemini client
        # The client handles connection pooling, authentication, and retries
        try:
            self.client: genai.Client = genai.Client(api_key=api_key)
        except Exception as e:
            raise GeminiServiceException(
                "Failed to initialize Gemini client",
                original_error=e,
                error_code="CLIENT_INIT_FAILED"
            )
        
        # Store default configuration for reuse
        self.default_model: str = DEFAULT_MODEL
    
    def generate_text(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Google's Gemini API.
        
        This is the primary method for AI text generation. It sends a prompt
to the Gemini API and returns the generated response as plain text.
        
        Args:
            prompt: The text prompt to send to Gemini.
                   Should be clear and specific for best results.
            model_name: Specific Gemini model to use.
                       Defaults to DEFAULT_MODEL if not specified.
                       Options: gemini-2.5-flash, gemini-2.5-pro, etc.
            temperature: Controls response creativity (0.0-1.0).
                        Lower = more deterministic, higher = more creative.
            max_tokens: Maximum tokens in the response.
                       Default 2048 tokens is usually sufficient.
                       
        Returns:
            str: The generated text response from Gemini.
            
        Raises:
            GeminiServiceException: If API call fails, returns empty response,
                                   or encounters network issues.
            
        Example - Simple usage:
            >>> service = GeminiService()
            >>> response = service.generate_text(
            ...     "Explain air pollution in one sentence."
            ... )
            >>> print(response)
            "Air pollution is the contamination of air by harmful substances..."
            
        Example - Advanced usage:
            >>> response = service.generate_text(
            ...     prompt="Analyze this data trend for air quality...",
            ...     model_name="gemini-2.5-pro",  # Use pro for complex analysis
            ...     temperature=0.3,  # Lower for more factual output
            ...     max_tokens=4096  # Longer for detailed analysis
            ... )
            
        Example - Error handling:
            >>> try:
            ...     response = service.generate_text("prompt")
            ... except GeminiServiceException as e:
            ...     if e.error_code == "MISSING_API_KEY":
            ...         print("Please configure your API key")
            ...     else:
            ...         print(f"API error: {e.message}")
            
        Best Practices:
            - Be specific in prompts for better responses
            - Handle exceptions in production code
            - Use appropriate temperature for your use case
            - Set max_tokens to control costs
            - Consider caching responses for repeated queries
            
        Performance:
            - First call may be slower (connection warmup)
            - Subsequent calls reuse connections
            - Consider async implementation for high throughput
        """
        # VALIDATION: Check for empty prompt
        if not prompt or len(prompt.strip()) == 0:
            raise GeminiServiceException(
                "Prompt cannot be empty",
                error_code="EMPTY_PROMPT"
            )
        
        # Use provided model or fall back to default
        model: str = model_name if model_name else self.default_model
        
        # Use provided parameters or fall back to defaults
        temp: float = temperature if temperature is not None else DEFAULT_TEMPERATURE
        tokens: int = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
        
        try:
            # Generate content using Gemini API
            # The client.chat.completions.create mimics OpenAI interface
            # but uses Gemini models under the hood
            response = self.client.models.generate_content(
                model=model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    temperature=temp,
                    max_output_tokens=tokens,
                )
            )
            
            # VALIDATION: Check for empty response
            # Gemini may return empty content for certain prompts or failures
            if not response or not response.text:
                raise GeminiServiceException(
                    "Gemini returned an empty response. "
                    "This may indicate a filtered prompt or API issue.",
                    error_code="EMPTY_RESPONSE"
                )
            
            return response.text
            
        except GeminiServiceException:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            # Wrap all other exceptions for consistent error handling
            raise GeminiServiceException(
                f"Failed to generate text using Gemini API",
                original_error=e,
                error_code="API_ERROR"
            )


# =============================================================================
# EXAMPLE USAGE
# =============================================================================
# This section demonstrates how to use the GeminiService in practice.
# Run this file directly to test the service (requires API key).

if __name__ == "__main__":
    # Example 1: Basic usage
    print("=" * 50)
    print("Example 1: Basic Text Generation")
    print("=" * 50)
    
    try:
        # Create service instance (one per application)
        service = GeminiService()
        
        # Simple prompt
        response = service.generate_text(
            "Explain air pollution in one sentence."
        )
        print(f"Response: {response}")
        
    except GeminiServiceException as e:
        print(f"Error: {e.message}")
        print(f"Error code: {e.error_code}")
    
    print()
    
    # Example 2: Using specific model
    print("=" * 50)
    print("Example 2: Using Gemini Pro Model")
    print("=" * 50)
    
    try:
        service = GeminiService()
        
        # Use pro model for more complex analysis
        response = service.generate_text(
            prompt="Analyze the impact of urban traffic on air quality.",
            model_name="gemini-2.5-pro",
            temperature=0.5,
            max_tokens=1024
        )
        print(f"Response: {response}")
        
    except GeminiServiceException as e:
        print(f"Error: {e.message}")
        
    print()
    
    # Example 3: Error handling
    print("=" * 50)
    print("Example 3: Error Handling Demo")
    print("=" * 50)
    
    try:
        # This will fail because prompt is empty
        service = GeminiService()
        response = service.generate_text("")
        
    except GeminiServiceException as e:
        print(f"Caught exception: {e}")
        print(f"Error code: {e.error_code}")
        print(f"Original error: {e.original_error}")
