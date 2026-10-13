"""Starter FDE: validated inbound API to deterministic synthetic CRM."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.features.crm_client import send_to_crm, CrmError

app = FastAPI(title="Enterprise API Integration Gateway")
class Request(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
class Result(BaseModel):
    status: str
    crm_id: str

@app.post("/process", response_model=Result)
def process(request: Request) -> Result:
    """Never forward unvalidated input or expose server-side credentials."""
    try:
        response = send_to_crm(request.message)
    except CrmError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.public_message) from exc
    return Result(status="accepted", crm_id=response["crm_id"])

# Persist request/outcome metadata independently from synthetic CRM calls.
from app.core.request_audit_middleware import RequestAuditMiddleware
app.add_middleware(RequestAuditMiddleware)
