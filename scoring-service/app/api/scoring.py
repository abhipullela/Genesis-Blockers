import pandas as pd
from fastapi import APIRouter

from app.explainability.reasons import ReasonGenerator
from app.ml.model_loader import ModelLoader
from app.schemas.scoring import (
    ScoringRequest,
    ScoringResponse,
)
from app.scoring.baseline import BaselineScorer
from app.scoring.hybrid import HybridScorer
from app.scoring.risk import RiskScorer

router = APIRouter()

baseline_scorer = BaselineScorer()
hybrid_scorer = HybridScorer()
reason_generator = ReasonGenerator()
risk_scorer = RiskScorer()

model_loader = ModelLoader().load()


@router.post(
    "/scoring/calculate",
    response_model=ScoringResponse,
)
def calculate_score(request: ScoringRequest):

    features = request.features.model_dump()

    # Rule-based baseline
    baseline_confidence = baseline_scorer.score(
        features
    )

    # ML prediction
    ml_probability = model_loader.predict_proba(
        pd.DataFrame([features])
    )[0]

    # Hybrid attribution confidence
    confidence = hybrid_scorer.score(
        ml_probability=ml_probability,
        baseline_confidence=baseline_confidence,
    )
    if confidence >= 0.70:
        attribution_status = "HIGH_CONFIDENCE"
    elif confidence >= 0.50:
        attribution_status = "MEDIUM_CONFIDENCE"
    else:
        attribution_status = "INCONCLUSIVE"

    # Risk
    risk_score = risk_scorer.score(features)
    risk_level = risk_scorer.risk_level(
        risk_score
    )

    # Explanation
    reasons = reason_generator.generate(features)

    return ScoringResponse(
        vasp_id=request.candidate_vasp.vasp_id,
        vasp_name=request.candidate_vasp.vasp_name,

        confidence=confidence,
        ml_probability=round(ml_probability, 4),
        baseline_confidence=round(baseline_confidence, 4),
        model_version="rf-v1",

        attribution_status=attribution_status,

        risk_score=risk_score,
        risk_level=risk_level,
        reasons=reasons,
    )