from app.features.builder import FeatureBuilder


def test_build_candidate():
    candidate = {
        "address": "0x123",
        "graph_distance": 2,
        "transaction_count": 3,
        "address_confidence": 0.95,
        "path_strength": 0.3333,
        "vasp": {
            "known": True,
            "confidence": 0.95,
        },
    }

    builder = FeatureBuilder()
    features = builder.build_candidate(candidate)

    assert features["graph_distance"] == 2
    assert features["transaction_count"] == 3
    assert features["address_confidence"] == 0.95
    assert features["path_strength"] == 0.3333
    assert features["known_address_match"] is True


def test_build_graph_response():
    graph_response = {
        "success": True,
        "data": {
            "input_wallet": "0x111",
            "vasp_matches": [
                {
                    "address": "0x222",
                    "graph_distance": 1,
                    "transaction_count": 1,
                    "address_confidence": 0.98,
                    "path_strength": 0.5,
                    "vasp": {
                        "known": True,
                        "vasp_id": "vasp_001",
                        "vasp_name": "Demo VASP",
                        "confidence": 0.98,
                    },
                },
                {
                    "address": "0x333",
                    "graph_distance": 4,
                    "transaction_count": 4,
                    "address_confidence": 0.55,
                    "path_strength": 0.2,
                    "vasp": {
                        "known": True,
                        "vasp_id": "vasp_002",
                        "vasp_name": "Second Demo VASP",
                        "confidence": 0.55,
                    },
                },
            ],
        },
    }

    builder = FeatureBuilder()
    features = builder.build_response(graph_response)

    assert len(features) == 2

    assert features[0]["vasp_id"] == "vasp_001"
    assert features[0]["vasp_name"] == "Demo VASP"
    assert features[0]["graph_distance"] == 1
    assert features[0]["address_confidence"] == 0.98

    assert features[1]["vasp_id"] == "vasp_002"
    assert features[1]["vasp_name"] == "Second Demo VASP"
    assert features[1]["graph_distance"] == 4
    assert features[1]["address_confidence"] == 0.55