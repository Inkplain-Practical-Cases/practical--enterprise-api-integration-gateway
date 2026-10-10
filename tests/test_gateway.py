"""Contract tests use only the deterministic CRM httpx MockTransport."""
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_validated_request():
    result = client.post("/process", json={"message": "synthetic order"})
    assert result.status_code == 200
    assert result.json()["status"] == "accepted"
    assert result.json()["crm_id"].startswith("crm-")

def test_missing_field():
    assert client.post("/process", json={}).status_code == 422

def test_empty_field():
    assert client.post("/process", json={"message": ""}).status_code == 422

def test_max_length():
    assert client.post("/process", json={"message": "x" * 2001}).status_code == 422

def test_missing_token_fails_closed(monkeypatch):
    monkeypatch.setenv("CRM_API_TOKEN", "")
    result = client.post("/process", json={"message": "synthetic order"})
    assert result.status_code == 503
    assert "offline-demo" not in result.text

def test_upstream_timeout():
    assert client.post("/process", json={"message": "timeout"}).status_code == 504

def test_upstream_unavailable():
    assert client.post("/process", json={"message": "unavailable"}).status_code == 503

def test_invalid_upstream_response():
    assert client.post("/process", json={"message": "invalid-response"}).status_code == 502

