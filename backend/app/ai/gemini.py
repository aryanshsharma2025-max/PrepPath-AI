import time
import logging
from typing import Any, Dict, Optional
from google import genai
from google.genai import types
from app.config import settings

logger = logging.getLogger(__name__)

# Lazy singleton client instance
_gemini_client: Optional[genai.Client] = None


def get_gemini_client() -> genai.Client:
    """
    Returns a lazy-singleton instance of google.genai.Client.

    Raises
    ------
    ValueError
        If GEMINI_API_KEY is not configured in settings.
    """
    global _gemini_client

    if _gemini_client is not None:
        return _gemini_client

    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "Gemini API key is not configured. Set GEMINI_API_KEY environment variable."
        )

    _gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _gemini_client


def generate_text(prompt: str, model: Optional[str] = None) -> str:
    """
    Generate plain text response using Gemini with retry for transient rate limits.
    """
    client = get_gemini_client()
    target_model = model or settings.GEMINI_MODEL

    last_err = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
            )
            return response.text
        except Exception as err:
            last_err = err
            if "429" in str(err) or "RESOURCE_EXHAUSTED" in str(err):
                logger.warning(f"Gemini API rate limit hit (attempt {attempt+1}/3), backing off 2.5s...")
                time.sleep(2.5)
                continue
            logger.error(f"Gemini text generation failed for model '{target_model}': {type(err).__name__}")
            raise RuntimeError(f"Gemini text generation failed: {type(err).__name__}") from err

    logger.error(f"Gemini text generation failed after retries for model '{target_model}': {type(last_err).__name__}")
    raise RuntimeError(f"Gemini text generation failed: {type(last_err).__name__}") from last_err


def generate_structured(
    prompt: str,
    response_schema: Optional[Any] = None,
    model: Optional[str] = None
) -> str:
    """
    Helper for generating structured JSON output with retry for transient rate limits.
    """
    client = get_gemini_client()
    target_model = model or settings.GEMINI_MODEL

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=response_schema if response_schema else None,
    )

    last_err = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as err:
            last_err = err
            if "429" in str(err) or "RESOURCE_EXHAUSTED" in str(err):
                logger.warning(f"Gemini API rate limit hit (attempt {attempt+1}/3), backing off 2.5s...")
                time.sleep(2.5)
                continue
            logger.error(f"Gemini structured generation failed for model '{target_model}': {type(err).__name__}")
            raise RuntimeError(f"Gemini structured generation failed: {type(err).__name__}") from err

    logger.error(f"Gemini structured generation failed after retries for model '{target_model}': {type(last_err).__name__}")
    raise RuntimeError(f"Gemini structured generation failed: {type(last_err).__name__}") from last_err

