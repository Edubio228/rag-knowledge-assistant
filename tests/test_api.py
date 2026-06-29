import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={"question": "What is the refund policy?", "top_k": 3}
    )
    assert response.status_code == 200
    assert "answer" in response.json()