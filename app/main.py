"""FastAPI door for synthetic CRM integration."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.features.step_2 import transform
app = FastAPI(title="Enterprise API Gateway")
class Request(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
@app.post("/process")
def process(request: Request) -> dict[str,str]:
    """Validate a request and call the offline CRM adapter."""
    return {"status":"accepted","result":transform(request.message)}
