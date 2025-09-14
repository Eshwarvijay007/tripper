from __future__ import annotations
import os
from typing import Any, Dict, Generator, Optional

import requests


class LangGraphAPI:
    """Thin client for calling a hosted LangGraph API.

    Configuration via environment variables:
    - LANGRAPH_REMOTE: "1"/"true" to force remote mode.
    - LANGRAPH_API_BASE: Base URL, e.g. https://api.langgraph.cloud/v1
    - LANGRAPH_GRAPH_ID: Graph/Deployment ID to target.
    - LANGRAPH_API_KEY: API key for x-api-key header (default).
    - LANGRAPH_AUTH_HEADER: Custom auth header name (default: x-api-key).
    - LANGRAPH_START_URL: Optional full URL override for starting runs.
    - LANGRAPH_STATUS_URL_TEMPLATE: Optional full URL template for status (use {run_id}).
    - LANGRAPH_STREAM_URL_TEMPLATE: Optional full URL template for SSE stream (use {run_id}).
    - LANGRAPH_INPUT_KEY: If set, wrap input into {INPUT_KEY: payload}. If unset, send payload as-is.
    """

    def __init__(self) -> None:
        self.remote_flag = (os.getenv("LANGRAPH_REMOTE") or "").strip().lower() in {"1", "true", "yes"}
        self.base = (os.getenv("LANGRAPH_API_BASE") or "").rstrip("/")
        self.graph_id = os.getenv("LANGRAPH_GRAPH_ID") or ""
        self.api_key = os.getenv("LANGRAPH_API_KEY") or ""
        self.auth_header = os.getenv("LANGRAPH_AUTH_HEADER") or "x-api-key"
        self.start_url_override = os.getenv("LANGRAPH_START_URL")
        self.status_url_tmpl = os.getenv("LANGRAPH_STATUS_URL_TEMPLATE")
        self.stream_url_tmpl = os.getenv("LANGRAPH_STREAM_URL_TEMPLATE")
        self.input_key = os.getenv("LANGRAPH_INPUT_KEY")
        # Optional scoping/auth details
        self.org_id = os.getenv("LANGRAPH_ORG_ID") or os.getenv("ORG_ID")
        self.workspace_id = os.getenv("LANGRAPH_WORKSPACE_ID") or os.getenv("WORKSPACE_ID")
        self.auth_scheme = os.getenv("LANGRAPH_AUTH_SCHEME")  # e.g., "Bearer"

    def is_enabled(self) -> bool:
        if self.remote_flag:
            return True
        # Enable if base+graph+key are present
        return bool(self.base and self.graph_id and self.api_key)

    # URL builders (with sensible defaults for LangGraph Cloud-style APIs)
    def _start_url(self) -> str:
        if self.start_url_override:
            return self.start_url_override
        if not (self.base and self.graph_id):
            raise RuntimeError("LangGraph API not configured: set LANGRAPH_API_BASE and LANGRAPH_GRAPH_ID or LANGRAPH_START_URL")
        return f"{self.base}/graphs/{self.graph_id}/runs"

    def _status_url(self, run_id: str) -> str:
        if self.status_url_tmpl:
            return self.status_url_tmpl.format(run_id=run_id)
        if not self.base:
            raise RuntimeError("LangGraph API base not configured: set LANGRAPH_API_BASE or LANGRAPH_STATUS_URL_TEMPLATE")
        return f"{self.base}/runs/{run_id}"

    def _stream_url(self, run_id: str) -> str:
        if self.stream_url_tmpl:
            return self.stream_url_tmpl.format(run_id=run_id)
        if not self.base:
            raise RuntimeError("LangGraph API base not configured: set LANGRAPH_API_BASE or LANGRAPH_STREAM_URL_TEMPLATE")
        return f"{self.base}/runs/{run_id}/stream"

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
        }
        if self.api_key:
            if self.auth_scheme and self.auth_scheme.lower() == "bearer":
                headers["Authorization"] = f"Bearer {self.api_key}"
            else:
                headers[self.auth_header] = self.api_key
        if self.org_id:
            headers.setdefault("x-org-id", self.org_id)
        if self.workspace_id:
            headers.setdefault("x-workspace-id", self.workspace_id)
        return headers

    def start_itinerary_run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Start a remote run. Returns server response JSON, expected to include an id."""
        url = self._start_url()
        body: Dict[str, Any]
        if self.input_key:
            body = {self.input_key: payload}
        else:
            body = payload
        resp = requests.post(url, json=body, headers=self._headers(), timeout=60)
        resp.raise_for_status()
        return resp.json()

    def get_run_status(self, run_id: str) -> Dict[str, Any]:
        url = self._status_url(run_id)
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def stream_run(self, run_id: str) -> Generator[bytes, None, None]:
        """Proxy the remote event stream as bytes."""
        url = self._stream_url(run_id)
        headers = self._headers()
        # Many LangGraph streams are SSE; keep headers permissive
        headers.setdefault("Accept", "text/event-stream, application/json;q=0.9, */*;q=0.8")
        with requests.get(url, headers=headers, stream=True, timeout=300) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk
