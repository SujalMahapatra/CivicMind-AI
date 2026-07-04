"""
CivicMind AI - Gemini Service

Centralized Gemini AI integration service for CivicMind AI.

This service acts as the single entry point between the application and
Google's Gemini API. All AI-powered agents should use this service instead
of directly interacting with the Gemini SDK.

## AGENTS USING THIS SERVICE:

* Insight Agent
* Recommendation Agent
* Report Agent
* RAG Agent

## WHY USE A SERVICE LAYER?

Benefits of centralizing Gemini integration:

1. Reusability
   One implementation shared across all agents.

2. Maintainability
   If Google changes the SDK, only this file needs updating.

3. Consistent Error Handling
   All Gemini-related exceptions are handled uniformly.

4. Configuration Management
   API keys and model selection remain centralized.

5. Future Enhancements
   Retry logic, caching, logging, rate limiting, and monitoring
   can be added in one place.
   """

from typing import Optional

from google import genai
from google.genai import types

from config import settings

class GeminiServiceException(Exception):
    """
    Custom exception for Gemini service related failures.

    ```
    Attributes:
        message:
            Human-readable error description.

        original_error:
            Underlying exception if available.

        error_code:
            Optional classification for easier debugging.
    """

    def __init__(
        self,
        message: str,
        original_error: Optional[Exception] = None,
        error_code: Optional[str] = None
    ) -> None:
        super().__init__(message)

        self.message = message
        self.original_error = original_error
        self.error_code = error_code

    def __str__(self) -> str:
        if self.original_error:
            return (
                f"{self.message} | "
                f"Original Error: {self.original_error}"
            )

        return self.message


class GeminiService:
    """
    Reusable Gemini API service.

    ```
    This service manages:
    - Gemini client initialization
    - Model selection
    - Prompt execution
    - Error handling

    Create once and reuse throughout the application.
    """

    # ============================================================
    # MODEL CONFIGURATION
    # ============================================================

    FLASH_MODEL: str = "gemini-2.5-flash"
    PRO_MODEL: str = "gemini-2.5-pro"

    DEFAULT_MODEL: str = FLASH_MODEL

    # ============================================================
    # GENERATION SETTINGS
    # ============================================================

    DEFAULT_TEMPERATURE: float = 0.7

    DEFAULT_MAX_TOKENS: int = 2048

    def __init__(self) -> None:
        """
        Initialize Gemini client.

        Validates API key configuration and creates a reusable
        Gemini client instance.
        """

        api_key: str = settings.GEMINI_API_KEY

        if not api_key or len(api_key.strip()) == 0:
            raise GeminiServiceException(
                message=(
                    "GEMINI_API_KEY is missing. "
                    "Please configure it in your .env file."
                ),
                error_code="MISSING_API_KEY"
            )

        try:
            self.client: genai.Client = genai.Client(
                api_key=api_key
            )

        except Exception as e:
            raise GeminiServiceException(
                message="Failed to initialize Gemini client.",
                original_error=e,
                error_code="CLIENT_INITIALIZATION_FAILED"
            )

        self.default_model: str = self.DEFAULT_MODEL

    def generate_text(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Gemini.

        Args:
            prompt:
                User prompt sent to Gemini.

            model_name:
                Optional model override.
                Example:
                    GeminiService.PRO_MODEL

            temperature:
                Creativity level.
                Lower values = more deterministic.

            max_tokens:
                Maximum response length.

        Returns:
            Generated text response.

        Raises:
            GeminiServiceException
        """

        if not prompt or len(prompt.strip()) == 0:
            raise GeminiServiceException(
                message="Prompt cannot be empty.",
                error_code="EMPTY_PROMPT"
            )

        selected_model: str = (
            model_name
            if model_name
            else self.default_model
        )

        selected_temperature: float = (
            temperature
            if temperature is not None
            else self.DEFAULT_TEMPERATURE
        )

        selected_max_tokens: int = (
            max_tokens
            if max_tokens is not None
            else self.DEFAULT_MAX_TOKENS
        )

        try:
            response = self.client.models.generate_content(
                model=selected_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=selected_temperature,
                    max_output_tokens=selected_max_tokens,
                )
            )

            if (
                response is None
                or response.text is None
                or len(response.text.strip()) == 0
            ):
                raise GeminiServiceException(
                    message="Gemini returned an empty response.",
                    error_code="EMPTY_RESPONSE"
                )

            return response.text.strip()

        except GeminiServiceException:
            raise

        except Exception as e:
            raise GeminiServiceException(
                message="Failed to generate Gemini response.",
                original_error=e,
                error_code="API_ERROR"
            )


# ================================================================

# SHARED SINGLETON INSTANCE

# ================================================================

# Import and reuse this object throughout the application:

#

# from services.gemini_service import gemini_service

#

# This avoids repeatedly creating Gemini clients.

gemini_service = GeminiService()
"""
Shared application-wide Gemini service instance.
"""
