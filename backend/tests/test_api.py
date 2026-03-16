import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

@pytest.mark.asyncio
async def test_private_repo_gate(client):
    # Test that private repo analysis requires token
    response = await client.post("/api/analyze?repo_url=test/repo&is_private=true")
    assert response.status_code == 401
    assert "token" in response.json()["detail"].lower()
