from app.explainability.reasons import ReasonGenerator


def test_high_confidence_reasons():
    generator = ReasonGenerator()

    features = {
        "address_confidence": 0.98,
        "graph_distance": 1,
        "transaction_count": 1,
    }

    reasons = generator.generate(features)

    assert len(reasons) == 3
    assert "High-confidence VASP address match" in reasons
    assert "VASP address is directly connected to the wallet" in reasons
    assert "Only one transaction supports the connection" in reasons


def test_low_confidence_reasons():
    generator = ReasonGenerator()

    features = {
        "address_confidence": 0.35,
        "graph_distance": 5,
        "transaction_count": 5,
    }

    reasons = generator.generate(features)

    assert "Low-confidence VASP address match" in reasons
    assert "VASP address is 5 transaction hops away" in reasons
    assert "Multiple transactions support the connection" in reasons