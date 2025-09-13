from __future__ import annotations
from fastapi import APIRouter, HTTPException
from ..schemas.jobs import JobStatus
from ..services.store import JOBS

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobStatus)
def get_job(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(**job)

