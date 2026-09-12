from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_known_address():
    response = client.get(
        "/api/v1/vasp/address/"
        "0x1111111111111111111111111111111111111111"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["known"] is True
    assert data["data"]["vasp"]["vasp_id"] == "vasp_001"
    assert data["data"]["confidence"] == 0.95


def test_unknown_address():
    response = client.get(
        "/api/v1/vasp/address/"
        "0x2222222222222222222222222222222222222222"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["known"] is False
    assert data["data"]["vasp"] is None
    assert data["data"]["confidence"] == 0


def test_invalid_address():
    response = client.get(
        "/api/v1/vasp/address/hello"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_WALLET"