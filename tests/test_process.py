"""Contract checks for the synthetic CRM adapter."""
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_success():
    assert client.post("/process",json={"message":"Test"}).json()["result"]=="crm:Test"
def test_invalid():
    assert client.post("/process",json={}).status_code==422
