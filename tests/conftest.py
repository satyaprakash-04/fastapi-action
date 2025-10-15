# import pytest
# from app.main import app
# from httpx import AsyncClient, ASGITransport
# from fastapi.testclient import TestClient

# client = TestClient(app)

# @pytest.fixture
# async def async_client():
#     async with AsyncClient(app=client, base_url="http://testserver") as ac:
#         yield ac

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "price": 10.99})
    assert response.status_code == 200
    assert response.json() == {"item_id": "new_item", "name": "Test Item", "price": 10.99}

def test_create_item_invalid_data():
    response = client.post("/items/", json={"name": "Test Item"}) # Missing price
    assert response.status_code == 422 # 