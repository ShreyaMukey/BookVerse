import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from bookverse.main import create_app


@pytest.fixture
async def client():
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def credentials():
    return {"email": f"{uuid.uuid4()}@example.com", "password": "correcthorsebattery"}


@pytest.mark.asyncio
async def test_register_login_me_flow(client, credentials):
    register_response = await client.post("/api/auth/register", json=credentials)
    assert register_response.status_code == 201
    assert "access_token" in register_response.json()

    duplicate_response = await client.post("/api/auth/register", json=credentials)
    assert duplicate_response.status_code == 409

    bad_login_response = await client.post("/api/auth/login", json={"email": credentials["email"], "password": "wrong"})
    assert bad_login_response.status_code == 401

    login_response = await client.post("/api/auth/login", json=credentials)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["email"] == credentials["email"]


@pytest.mark.asyncio
async def test_register_rejects_short_password(client):
    response = await client.post(
        "/api/auth/register", json={"email": f"{uuid.uuid4()}@example.com", "password": "short"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_me_requires_token(client):
    no_token_response = await client.get("/api/auth/me")
    assert no_token_response.status_code == 401

    garbage_token_response = await client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"})
    assert garbage_token_response.status_code == 401
