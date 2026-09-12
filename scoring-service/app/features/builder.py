from typing import Any, Dict, List


class FeatureBuilder:
    """
    Converts Graph Service candidate evidence into
    numerical features used by the scoring system.
    """

    def build_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        vasp = candidate.get("vasp", {})

        return {
            "vasp_id": vasp.get("vasp_id"),
            "vasp_name": vasp.get("vasp_name"),
            "graph_distance": candidate.get("graph_distance", 0),
            "path_strength": candidate.get("path_strength", 0.0),
            "transaction_count": candidate.get("transaction_count", 0),
            "address_confidence": candidate.get(
                "address_confidence",
                0.0,
            ),
            "known_address_match": vasp.get(
                "known",
                False,
            ),
        }

    def build_response(
        self,
        graph_response: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Convert an entire Graph Service response into
        candidate-level feature records.
        """

        data = graph_response.get("data", {})
        candidates = data.get("vasp_matches", [])

        return [
            self.build_candidate(candidate)
            for candidate in candidates
        ]