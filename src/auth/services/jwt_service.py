"""Provides a service for creating and decoding JWT access and refresh tokens."""

import uuid
from datetime import datetime, timedelta, timezone
from gettext import gettext as _
from typing import Any

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from config.config.settings import user_settings as settings
from src.auth.shemas.token import TokenPayloadDTO


class JWTService:
    """Service for creating, decoding, and validating JWT tokens."""

    def __init__(self) -> None:
        """Initialize JWTService with secret, algorithm, and expiration settings."""
        self.secret_key: str = settings.SECRET_KEY
        self.algorithm: str = settings.ALGORITHM
        self.access_token_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days: int = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def create_token(self, data: dict[str, Any], expires_delta: timedelta) -> str:
        current_time: datetime = datetime.now(timezone.utc)
        expire: datetime = current_time + expires_delta  # aware datetime UTC

        to_encode = data.copy()
        to_encode.update({
            "exp": int(expire.timestamp()),  # передаем Unix timestamp (int)
            "jti": str(uuid.uuid4()),
        })

        encoded_jwt: str = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        print(f"Текущее время (UTC):  {current_time.isoformat()}")  # Вывод текущего времени
        print(f"Время истечения (UTC): {expire.isoformat()}")
        return encoded_jwt

    def create_access_token(self, data: dict[str, Any]) -> str:
        data_copy = data.copy()
        data_copy.update({"token_type": "access"})
        expires_delta: timedelta = timedelta(minutes=self.access_token_expire_minutes)
        return self.create_token(data_copy, expires_delta)

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        """Create a refresh token with a defined lifetime."""
        data.update({"token_type": "refresh"})
        expires_delta: timedelta = timedelta(days=self.refresh_token_expire_days)
        return self.create_token(data, expires_delta)

    def decode_token(self, token: str) -> TokenPayloadDTO:
        try:
            now = datetime.now(timezone.utc)
            print("Текущее время при декодировании (UTC):", now.isoformat())
            decoded_payload: dict[str, Any] = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print("Расшифрованный payload токена:", decoded_payload)
            return TokenPayloadDTO(**decoded_payload)
        except ExpiredSignatureError as err:
            raise ExpiredSignatureError(_("Token has expired.")) from err
        except InvalidTokenError as err:
            raise InvalidTokenError(_("Invalid token.")) from err
        except DecodeError as err:
            raise DecodeError(_("Token decoding error.")) from err
        except Exception as err:
            raise InvalidTokenError(_("Unknown error decoding token: {err}").format(err=err)) from err
