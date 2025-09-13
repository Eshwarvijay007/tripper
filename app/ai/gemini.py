from __future__ import annotations
import os
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover - optional until installed
    genai = None  # type: ignore


_configured = False


def _configure() -> None:
    global _configured
    if _configured:
        return
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # Defer strict error so the app can start without LLM usage
        return
    if genai is None:
        raise RuntimeError("google-generativeai package not installed; add to requirements.txt")
    genai.configure(api_key=api_key)
    _configured = True


def gemini_json(
    prompt: str,
    *,
    system: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 4096,
) -> Dict[str, Any]:
    """Call Gemini and return parsed JSON.

    Raises RuntimeError on configuration or generation errors.
    """
    _configure()
    if genai is None:
        raise RuntimeError("Gemini client unavailable")

    model_name = model or os.getenv("GEMINI_MODEL") or "gemini-1.5-flash"
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": "application/json",
    }
    model_client = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
    parts = [prompt]
    if system:
        parts = [f"SYSTEM:\n{system}\n\nUSER:\n{prompt}"]
    try:
        resp = model_client.generate_content(parts)
        text = resp.text or "{}"
        # Some SDK versions provide .candidates[0].content.parts; fall back to .text
        import json
        return json.loads(text)
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Gemini JSON generation failed: {e}")


def gemini_text(
    prompt: str,
    *,
    system: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.5,
    max_output_tokens: int = 2048,
) -> str:
    _configure()
    if genai is None:
        raise RuntimeError("Gemini client unavailable")
    model_name = model or os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    model_client = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
    parts = [prompt]
    if system:
        parts = [f"SYSTEM:\n{system}\n\nUSER:\n{prompt}"]
    try:
        resp = model_client.generate_content(parts)
        return resp.text or ""
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Gemini text generation failed: {e}")
