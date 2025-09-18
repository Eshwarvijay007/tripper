from __future__ import annotations
from typing import Any, Dict, List


def get_text(output: Any) -> str:
    """Best-effort to extract plain text from LangChain/LLM outputs."""
    if output is None:
        return ""
    # Direct string
    if isinstance(output, str):
        return output
    # LangChain message with .content
    content = getattr(output, "content", None)
    if content is not None:
        if isinstance(content, str):
            return content
        if isinstance(content, list):  # e.g., Gemini parts
            parts: List[str] = []
            for p in content:
                if isinstance(p, str):
                    parts.append(p)
                elif isinstance(p, dict) and "text" in p:
                    parts.append(str(p.get("text") or ""))
                else:
                    # Try common attribute
                    txt = getattr(p, "text", None)
                    if isinstance(txt, str):
                        parts.append(txt)
            return "".join(parts)
        # Fallback
        return str(content)
    # Common alternate attributes
    alt = getattr(output, "text", None) or getattr(output, "output_text", None)
    if isinstance(alt, str):
        return alt
    return str(output)


def coerce_json_text(value: Any) -> str:
    """Convert various content forms into a JSON-ish text for parsing."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        # It's already a dict, caller should treat as parsed
        return ""
    if isinstance(value, list):
        # Join textual parts
        parts: List[str] = []
        for p in value:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict) and "text" in p:
                parts.append(str(p.get("text") or ""))
            else:
                txt = getattr(p, "text", None)
                if isinstance(txt, str):
                    parts.append(txt)
        return "".join(parts)
    return str(value)

