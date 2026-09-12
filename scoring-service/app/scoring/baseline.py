from typing import Any, Dict


class BaselineScorer:
    """
    Transparent rule-based confidence scorer.

    Produces a confidence score between 0 and 1
    from VASP attribution evidence.
    """

    def score(self, features: Dict[str, Any]) -> float:
        """
        Calculate attribution confidence.
        """

        address_confidence = features.get(
            "address_confidence",
            0.0,
        )

        graph_distance = features.get(
            "graph_distance",
            0,
        )

        transaction_count = features.get(
            "transaction_count",
            0,
        )

        # Closer graph distance = stronger evidence.
        graph_score = 1.0 / (1.0 + graph_distance)

        # More transactions provide stronger supporting evidence,
        # but cap the contribution at 5 transactions.
        transaction_score = min(
            transaction_count / 5.0,
            1.0,
        )

        confidence = (
            0.50 * address_confidence
            + 0.30 * graph_score
            + 0.20 * transaction_score
        )

        return round(
            min(max(confidence, 0.0), 1.0),
            4,
        )