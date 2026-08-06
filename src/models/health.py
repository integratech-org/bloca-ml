from pydantic import BaseModel


class HealthResponse(BaseModel):
    is_healthy: bool
    message: str = "ok"
