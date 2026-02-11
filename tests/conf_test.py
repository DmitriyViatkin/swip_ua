from asyncio import Barrier

import pytest
from fastapi.testclient import TestClient
from config.app  import app
from src.auth.services.jwt_service import JWTService
from httpx import AsyncClient

@pytest.fixture(scope="session")
def client():
    """Створюємо клієнт для всього циклу тестів."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_headers(client):
    """
        Фікстура для логіну.
        Використовує JSON, як зазначено у твоєму LoginRequest.
    """
    login_payload  = {
        "username": "viatkindima@gmail.com",
        "password": "string1"
    }
    response = client.post("/auth/login", json=login_payload)
    if response.status_code != 200:
        pytest.fail(f"Login failed:{response.text}")
    data = response.json()
    token = data["access_token"]
    return{"Authorization": f"Bearer {token}"}


@pytest.fixture
async def second_user_headers(client: AsyncClient):
    """Створює другого користувача та повертає його токен для тестів доступу."""

    user_data = {
        "email": "second_user@test.com",
        "password": "password123",
        "full_name": "Stranger"
    }

    client.post("/auth/register", json=user_data)

    # Логинимся вторым пользователем
    login_resp = client.post("/auth/login", json={
        "username": user_data["email"],
        "password": user_data["password"]
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}