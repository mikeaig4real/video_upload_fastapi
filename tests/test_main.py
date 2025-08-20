from app.core.config import get_config
from main import app
from fastapi.testclient import TestClient
config = get_config()

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
