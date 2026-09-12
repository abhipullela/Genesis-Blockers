from typing import Any

import pandas as pd

from app.scoring.baseline import BaselineScorer


class CandidateRanker:
    """
    Scores and ranks VASP candidates for each investigation case.
    """

    def __init__(self):
        self.scorer = BaselineScorer()

    def rank(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate baseline confidence for every candidate
        and rank candidates within each case.
        """

        dataset = dataset.copy()

        dataset["confidence"] = dataset.apply(
            lambda row: self.scorer.score(
                {
                    "graph_distance": row["graph_distance"],
                    "transaction_count": row["transaction_count"],
                    "address_confidence": row["address_confidence"],
                }
            ),
            axis=1,
        )

        dataset["rank"] = (
            dataset.groupby("case_id")["confidence"]
            .rank(
                method="dense",
                ascending=False,
            )
            .astype(int)
        )

        return dataset.sort_values(
            ["case_id", "rank"]
        ).reset_index(drop=True)