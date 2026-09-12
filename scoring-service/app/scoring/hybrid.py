from typing import Any, Dict


class HybridScorer:
    """
    Combines the ML prediction with the transparent
    rule-based baseline score.
    """

    def __init__(
        self,
        ml_weight: float = 0.50,
        baseline_weight: float = 0.50,
    ):
        if ml_weight < 0 or baseline_weight < 0:
            raise ValueError("Weights must be non-negative")

        if ml_weight + baseline_weight == 0:
            raise ValueError("At least one weight must be greater than zero")

        total = ml_weight + baseline_weight

        self.ml_weight = ml_weight / total
        self.baseline_weight = baseline_weight / total

    def score(
        self,
        ml_probability: float,
        baseline_confidence: float,
    ) -> float:

        ml_probability = min(max(ml_probability, 0.0), 1.0)
        baseline_confidence = min(
            max(baseline_confidence, 0.0),
            1.0,
        )

        hybrid_score = (
            self.ml_weight * ml_probability
            + self.baseline_weight * baseline_confidence
        )

        return round(
            min(max(hybrid_score, 0.0), 1.0),
            4,
        )