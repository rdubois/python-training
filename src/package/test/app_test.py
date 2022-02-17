from fastapi.testclient import TestClient

from ..app import app

client = TestClient(app)

def test_alive():
    response = client.get("/alive")
    assert response.status_code == 204

def test_ready():
    response = client.get("/alive")
    assert response.status_code == 204