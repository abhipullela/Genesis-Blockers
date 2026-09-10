from datetime import datetime, timezone

from app.database import SessionLocal
from app.models import VASP, Source, VASPAddress


def seed_data():
    db = SessionLocal()

    try:
        # Demo VASP
        vasp = VASP(
            vasp_id="vasp_001",
            name="Demo VASP",
            country="IN",
            supported_chains="ethereum",
        )

        # Demo intelligence source
        source = Source(
            source_id="SOURCE-001",
            name="Verified Intelligence Source",
            type="public",
            reference="demo-source",
            verified_at=datetime.now(timezone.utc),
        )

        # Demo blockchain address
        address = VASPAddress(
            address="0x1111111111111111111111111111111111111111",
            chain="ethereum",
            vasp_id="vasp_001",
            address_type="deposit_address",
            confidence=0.95,
            source_id="SOURCE-001",
            last_verified=datetime.now(timezone.utc),
        )

        db.add(vasp)
        db.add(source)
        db.add(address)

        db.commit()

        print("✅ Demo data inserted successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()