from fastapi import APIRouter

from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
)


router = APIRouter(
    prefix="/investigate",
    tags=["Investigation"],
)


@router.post("", response_model=InvestigationResponse)
def investigate(request: InvestigationRequest):
    return InvestigationResponse(
        investigation_id="INV-DEMO-001",
        wallet=request.wallet,
        chain=request.chain,
        status="pending",
        message="Investigation pipeline not connected yet.",
    )