from typing import Any, Dict


class RiskScorer:
    """
    Calculates a wallet/transaction risk score from
    explicit risk indicators.

    The score is independent of VASP attribution confidence.
    """

    def score(self, features: Dict[str, Any]) -> int:
        risk_indicators = features.get(
            "risk_indicators",
            {}
        )

        high_risk_exposure = min(
            max(
                risk_indicators.get(
                    "high_risk_exposure",
                    0.0,
                ),
                0.0,
            ),
            1.0,
        )

        suspicious_transaction_ratio = min(
            max(
                risk_indicators.get(
                    "suspicious_transaction_ratio",
                    0.0,
                ),
                0.0,
            ),
            1.0,
        )

        rapid_transaction_activity = min(
            max(
                risk_indicators.get(
                    "rapid_transaction_activity",
                    0.0,
                ),
                0.0,
            ),
            1.0,
        )

        risk_score = (
            0.50 * high_risk_exposure
            + 0.30 * suspicious_transaction_ratio
            + 0.20 * rapid_transaction_activity
        )

        return round(risk_score * 100)

    def risk_level(self, risk_score: int) -> str:
        if risk_score >= 75:
            return "CRITICAL"
        elif risk_score >= 50:
            return "HIGH"
        elif risk_score >= 25:
            return "MEDIUM"
        else:
            return "LOW"