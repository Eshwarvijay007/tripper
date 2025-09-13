from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class JobStatus(BaseModel):
    id: str
    status: str  # pending | running | completed | failed
    result_type: Optional[str] = None
    result_id: Optional[str] = None
    error: Optional[str] = None

