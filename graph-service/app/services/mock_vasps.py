MOCK_VASP_ADDRESSES = {
    "0x2222222222222222222222222222222222222222": {
        "known": True,
        "vasp_id": "VASP-DEMO-001",
        "name": "Demo Exchange",
        "country": "IN",
        "confidence": 0.95,
        "source": "mock",
    }
}


def check_mock_vasp(address: str):
    return MOCK_VASP_ADDRESSES.get(
        address.lower(),
        {
            "known": False,
            "vasp_id": None,
            "name": None,
            "country": None,
            "confidence": 0.0,
            "source": "mock",
        },
    )