"""Accurate offline gateway contract tests for STEP-5."""
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_valid_request():
    result = client.post("/process", json={"message": "synthetic sample"})
    assert result.status_code == 200
    assert result.json()["status"] == "accepted"
    assert result.json()["crm_id"].startswith("crm-")

def test_required_message():
    assert client.post("/process", json={}).status_code == 422

def test_invalid_length():
    assert client.post("/process", json={"message": "x" * 2001}).status_code == 422

def test_configuration_required(monkeypatch):
    monkeypatch.setenv("CRM_API_TOKEN", "")
    assert client.post("/process", json={"message": "sample"}).status_code == 503

def test_upstream_failure():
    assert client.post("/process", json={"message": "unavailable"}).status_code == 503

def test_timeout():
    assert client.post("/process", json={"message": "timeout"}).status_code == 504
