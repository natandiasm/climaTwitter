import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_main_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"name": "ClimaTwitter", "version": os.getenv("VERSION")}