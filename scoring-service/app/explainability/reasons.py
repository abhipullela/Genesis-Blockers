from typing import Any, Dict, List


class ReasonGenerator:
    """
    Generates human-readable explanations for
    VASP attribution confidence scores.
    """

    def generate(
        self,
        features: Dict[str, Any],
    ) -> List[str]:
        reasons = []

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

        if address_confidence >= 0.90:
            reasons.append(
                "High-confidence VASP address match"
            )
        elif address_confidence >= 0.70:
            reasons.append(
                "Moderate-confidence VASP address match"
            )
        else:
            reasons.append(
                "Low-confidence VASP address match"
            )

        if graph_distance == 0:
            reasons.append(
                "Candidate address is the investigated wallet"
            )
        elif graph_distance == 1:
            reasons.append(
                "VASP address is directly connected to the wallet"
            )
        elif graph_distance <= 3:
            reasons.append(
                f"VASP address is within {graph_distance} transaction hops"
            )
        else:
            reasons.append(
                f"VASP address is {graph_distance} transaction hops away"
            )

        if transaction_count >= 5:
            reasons.append(
                "Multiple transactions support the connection"
            )
        elif transaction_count >= 2:
            reasons.append(
                "Several transactions support the connection"
            )
        elif transaction_count == 1:
            reasons.append(
                "Only one transaction supports the connection"
            )
        else:
            reasons.append(
                "No transaction evidence was found on the path"
            )

        return reasons