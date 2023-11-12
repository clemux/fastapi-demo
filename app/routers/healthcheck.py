from fastapi import APIRouter

from app.schemas.healthcheck import HealthcheckResponseSchema

router = APIRouter()


@router.get("/health", response_model=HealthcheckResponseSchema)
def healthcheck():
    return {"status": "ok"}
