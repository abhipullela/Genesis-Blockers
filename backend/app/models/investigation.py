from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    wallet: str = Field(..., min_length=1)
    chain: str = "ethereum"
    max_hops: int = Field(default=5, ge=1, le=20)


class InvestigationResponse(BaseModel):
    investigation_id: str
    wallet: str
    chain: str
    status: str
    message: str