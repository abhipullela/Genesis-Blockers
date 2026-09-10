from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import VASPAddress, VASP, Source

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/vasp/address/{address}")
def lookup_address(
    address: str,
    db: Session = Depends(get_db),
):
    # Basic Ethereum address validation
    if not address.startswith("0x") or len(address) != 42:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_WALLET",
                "message": "Invalid Ethereum address",
            },
        }

    # Look up the address
    record = (
        db.query(VASPAddress)
        .filter(VASPAddress.address == address)
        .first()
    )

    # Address not found
    if record is None:
        return {
            "success": True,
            "data": {
                "address": address,
                "chain": "ethereum",
                "known": False,
                "vasp": None,
                "address_type": None,
                "confidence": 0,
                "source": None,
            },
            "error": None,
        }

    # Get related VASP
    vasp = (
        db.query(VASP)
        .filter(VASP.vasp_id == record.vasp_id)
        .first()
    )

    # Get source
    source = (
        db.query(Source)
        .filter(Source.source_id == record.source_id)
        .first()
    )

    return {
        "success": True,
        "data": {
            "address": record.address,
            "chain": record.chain,
            "known": True,
            "vasp": {
                "vasp_id": vasp.vasp_id,
                "name": vasp.name,
                "country": vasp.country,
            },
            "address_type": record.address_type,
            "confidence": record.confidence,
            "source": source.source_id if source else None,
        },
        "error": None,
    }