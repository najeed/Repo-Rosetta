import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
import os

@pytest.fixture
async def client():
    # Force mock env vars for testing if necessary
    os.environ["GITHUB_CLIENT_ID"] = "test_id"
    os.environ["GITHUB_CLIENT_SECRET"] = "test_secret"
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
def setup_test_env():
    # Re-import to ensure env vars are picked up if modules use os.getenv at top level
    import importlib
    import backend.auth.github
    importlib.reload(backend.auth.github)
