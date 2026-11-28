import secrets

from fastapi import Security, status
from fastapi.exceptions import HTTPException
from fastapi.security.api_key import APIKeyHeader

from core.config import get_settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def api_key_auth(
    api_key: str | None = Security(api_key_header),
) -> str:
    settings = get_settings()

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "APIKey"},
        )

    if not secrets.compare_digest(api_key.encode(), settings.api_key.encode()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return api_key
