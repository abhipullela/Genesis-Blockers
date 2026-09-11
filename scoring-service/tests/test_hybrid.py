from app.scoring.hybrid import HybridScorer


def test_hybrid_score_equal_weights():
    scorer = HybridScorer()

    score = scorer.score(
        ml_probability=0.80,
        baseline_confidence=0.60,
    )

    assert score == 0.70


def test_hybrid_score_clamps_values():
    scorer = HybridScorer()

    score = scorer.score(
        ml_probability=1.5,
        baseline_confidence=-0.5,
    )

    assert score == 0.50


def test_hybrid_custom_weights():
    scorer = HybridScorer(
        ml_weight=0.70,
        baseline_weight=0.30,
    )

    score = scorer.score(
        ml_probability=0.90,
        baseline_confidence=0.50,
    )

    assert score == 0.78