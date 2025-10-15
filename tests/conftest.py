import pytest
from app.main import app
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac