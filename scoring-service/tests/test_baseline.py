from app.scoring.baseline import BaselineScorer


def test_high_confidence_candidate():
    scorer = BaselineScorer()

    features = {
        "graph_distance": 1,
        "transaction_count": 1,
        "address_confidence": 0.98,
    }

    score = scorer.score(features)

    assert 0.6 < score <= 1.0


def test_low_confidence_candidate():
    scorer = BaselineScorer()

    features = {
        "graph_distance": 5,
        "transaction_count": 5,
        "address_confidence": 0.40,
    }

    score = scorer.score(features)

    assert 0.0 <= score < 0.6


def test_score_is_bounded():
    scorer = BaselineScorer()

    features = {
        "graph_distance": 0,
        "transaction_count": 100,
        "address_confidence": 1.0,
    }

    score = scorer.score(features)

    assert 0.0 <= score <= 1.0