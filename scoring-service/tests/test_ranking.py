from app.features.dataset import DatasetLoader
from app.scoring.ranking import CandidateRanker


def test_candidate_ranking():
    dataset = DatasetLoader().load()

    ranker = CandidateRanker()
    ranked = ranker.rank(dataset)

    assert "confidence" in ranked.columns
    assert "rank" in ranked.columns

    assert ranked["confidence"].between(0.0, 1.0).all()

    case_001 = ranked[ranked["case_id"] == "001"]

    assert len(case_001) == 2
    assert case_001.iloc[0]["rank"] == 1
    assert case_001.iloc[1]["rank"] == 2

    assert (
        case_001.iloc[0]["confidence"]
        >= case_001.iloc[1]["confidence"]
    )
    assert case_001.iloc[0]["rank"] == 1