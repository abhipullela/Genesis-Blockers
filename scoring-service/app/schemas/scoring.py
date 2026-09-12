from pydantic import BaseModel, Field


class CandidateVASP(BaseModel):
    vasp_id: str
    vasp_name: str

class RiskIndicators(BaseModel):
    high_risk_exposure: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    suspicious_transaction_ratio: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    rapid_transaction_activity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

class ScoringFeatures(BaseModel):
    graph_distance: int = Field(ge=0)
    known_address_match: bool
    address_confidence: float = Field(ge=0.0, le=1.0)
    path_strength: float = Field(ge=0.0, le=1.0)
    transaction_count: int = Field(ge=0)

    risk_indicators: RiskIndicators = RiskIndicators()


class ScoringRequest(BaseModel):
    input_wallet: str
    candidate_vasp: CandidateVASP
    features: ScoringFeatures


class ScoringResponse(BaseModel):
    vasp_id: str
    vasp_name: str

    confidence: float
    ml_probability: float
    baseline_confidence: float
    model_version: str

    attribution_status: str

    risk_score: int
    risk_level: str
    reasons: list[str]