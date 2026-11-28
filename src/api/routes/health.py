from fastapi import APIRouter

from models.health import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(is_healthy=True)
