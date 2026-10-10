"""Synthetic gateway API contract tests: exact results, never an ambiguous 200-or-422 assertion."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_request_rejected():
    response = client.post('/process', json={})
    assert response.status_code == 422

def test_empty_message_rejected():
    response = client.post('/process', json={'message': ''})
    assert response.status_code == 422

def test_accepts_synthetic_message():
    response = client.post('/process', json={'message': 'synthetic sample'})
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'accepted'
    assert isinstance(data['result'], str)
    assert data['result'].startswith('verified:')

def test_rejects_excessive_length():
    assert client.post('/process', json={'message': 'x' * 2001}).status_code == 422
