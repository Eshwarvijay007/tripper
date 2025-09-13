from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/healthz")
def healthz():
    return {"status": "ok"}

