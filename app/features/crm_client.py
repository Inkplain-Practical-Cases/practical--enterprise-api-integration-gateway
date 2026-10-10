"""Offline httpx transport demonstrating authenticated CRM requests and bounded failures."""
import json
import os
import httpx

class CrmError(Exception):
    def __init__(self, status_code: int, public_message: str):
        self.status_code, self.public_message = status_code, public_message

def mock_crm_handler(request: httpx.Request) -> httpx.Response:
    """No network traffic. This fake intentionally models limited CRM behaviors."""
    if request.method != "POST" or str(request.url) != "https://crm.example.test/api/orders":
        return httpx.Response(404, json={"error": "unknown_route"})
    # Auth behavior is introduced in STEP-3.
    payload = json.loads(request.content.decode("utf-8"))
    message = payload["message"]
    # Timeout and normalized failure handling are introduced in STEP-4.
    return httpx.Response(201, json={"id": "crm-"+str(len(message))+"-"+message[:8].replace(" ","-"), "status": "created"})

def send_to_crm(message: str) -> dict[str, str]:
    """An injected local mock transport exercises the actual HTTP request path."""
    headers = {}
    # Credentials are introduced in STEP-3.
    try:
        with httpx.Client(transport=httpx.MockTransport(mock_crm_handler), timeout=2.0) as client:
            result = client.post("https://crm.example.test/api/orders",
                                 json={"message": message}, headers=headers)
    except httpx.TimeoutException as exc:
        raise CrmError(504, "CRM request timed out") from exc
    except httpx.RequestError as exc:
        raise CrmError(502, "CRM transport failed") from exc
    if result.status_code == 503:
        raise CrmError(503, "CRM temporarily unavailable")
    if result.status_code >= 400:
        raise CrmError(502, "CRM rejected the upstream request")
    try:
        payload = result.json()
        crm_id = payload["id"]
    except (ValueError, KeyError, TypeError) as exc:
        raise CrmError(502, "CRM returned an invalid response") from exc
    if not isinstance(crm_id, str) or not crm_id:
        raise CrmError(502, "CRM response is missing an identifier")
    return {"crm_id": crm_id}
