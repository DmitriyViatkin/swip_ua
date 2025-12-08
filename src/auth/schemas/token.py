from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TokenPayloadDTO(BaseModel):
    jti: str  # Уникальный идентификатор токена (JWT ID)
    exp: int = Field(..., description="Время истечения токена в формате UNIX timestamp")
    token_type: str  
    user_id: Optional[int] = None
    email: Optional[str] = None

    @property
    def expiration_datetime(self) -> datetime:
        """Возвращает время истечения токена в виде datetime."""
        return datetime.fromtimestamp(self.exp)