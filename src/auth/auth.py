'''
"""Provides a service for creating and decoding JWT access and refresh tokens."""

import uuid
from datetime import UTC, datetime, timedelta
from gettext import gettext as _
from typing import Any

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from src.main.config.settings import settings
from src.main.features.auth.dtos.token import TokenPayloadDTO


class JWTService:
    """Service for creating, decoding, and validating JWT tokens."""

    def __init__(self) -> None:
        """Initialize JWTService with secret, algorithm, and expiration settings."""
        self.secret_key: str = settings.SECRET_KEY
        self.algorithm: str = settings.ALGORITHM
        self.access_token_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days: int = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def create_token(self, data: dict[str, Any], expires_delta: timedelta) -> str:
        """Create a JWT token."""
        to_encode: dict[str, Any] = data.copy()
        expire: datetime = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
        encoded_jwt: str = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_access_token(self, data: dict[str, Any]) -> str:
        """Create an access token with a defined lifetime."""
        data.update({"token_type": "access"})
        expires_delta: timedelta = timedelta(minutes=self.access_token_expire_minutes)
        return self.create_token(data, expires_delta)

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        """Create a refresh token with a defined lifetime."""
        data.update({"token_type": "refresh"})
        expires_delta: timedelta = timedelta(days=self.refresh_token_expire_days)
        return self.create_token(data, expires_delta)

    def decode_token(self, token: str) -> TokenPayloadDTO:
        """Decode a JWT token and return its payload."""
        try:
            decoded_payload: dict[str, Any] = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayloadDTO(**decoded_payload)
        except ExpiredSignatureError as err:
            raise ExpiredSignatureError(_("Token has expired.")) from err
        except InvalidTokenError as err:
            raise InvalidTokenError(_("Invalid token.")) from err
        except DecodeError as err:
            raise DecodeError(_("Token decoding error.")) from err
        except Exception as err:
            raise InvalidTokenError(_("Unknown error decoding token: {err}").format(err=err)) from err
'''