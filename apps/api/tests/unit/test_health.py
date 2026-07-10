from httpx import ASGITransport, AsyncClient
import pytest
from bookverse.main import create_app


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
