from app.scoring.risk import RiskScorer


def test_low_risk():
    scorer = RiskScorer()

    features = {
        "risk_indicators": {
            "high_risk_exposure": 0.0,
            "suspicious_transaction_ratio": 0.0,
            "rapid_transaction_activity": 0.0,
        }
    }

    assert scorer.score(features) == 0


def test_high_risk():
    scorer = RiskScorer()

    features = {
        "risk_indicators": {
            "high_risk_exposure": 1.0,
            "suspicious_transaction_ratio": 1.0,
            "rapid_transaction_activity": 1.0,
        }
    }

    assert scorer.score(features) == 100


def test_partial_risk():
    scorer = RiskScorer()

    features = {
        "risk_indicators": {
            "high_risk_exposure": 0.8,
            "suspicious_transaction_ratio": 0.4,
            "rapid_transaction_activity": 0.5,
        }
    }

    score = scorer.score(features)

    assert score == 62