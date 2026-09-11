from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_scoring_calculate():
    response = client.post(
        "/api/v1/scoring/calculate",
        json={
            "input_wallet": (
                "0x1111111111111111111111111111111111111111"
            ),
            "candidate_vasp": {
                "vasp_id": "vasp_001",
                "vasp_name": "Demo Exchange A",
            },
            "features": {
                "graph_distance": 1,
                "known_address_match": True,
                "address_confidence": 0.98,
                "path_strength": 0.5,
                "transaction_count": 5,
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["vasp_id"] == "vasp_001"
    assert data["confidence"] >= 0.0
    assert data["confidence"] <= 1.0

    assert data["ml_probability"] >= 0.0
    assert data["ml_probability"] <= 1.0

    assert data["baseline_confidence"] >= 0.0
    assert data["baseline_confidence"] <= 1.0

    assert data["model_version"] == "rf-v1"

    assert data["attribution_status"] in [
        "HIGH_CONFIDENCE",
        "MEDIUM_CONFIDENCE",
        "INCONCLUSIVE",
    ]

    assert data["risk_level"] in [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    assert isinstance(data["reasons"], list)