import json
from pathlib import Path

import pandas as pd

from app.features.builder import FeatureBuilder


class DatasetLoader:
    """
    Loads synthetic Graph Service responses and their labels,
    then converts them into a tabular ML dataset.
    """

    def __init__(self, data_dir: str = "data/dummy"):
        self.data_dir = Path(data_dir)
        self.builder = FeatureBuilder()

    def load(self) -> pd.DataFrame:
        """
        Load all graph response JSON files and join them
        with labels.csv.
        """

        labels_path = self.data_dir / "labels.csv"

        labels = pd.read_csv(
            labels_path,
            dtype={
                "case_id": str,
                "candidate_vasp_id": str,
            },
        )

        records = []

        for file_path in sorted(self.data_dir.glob("graph_response_*.json")):
            case_id = file_path.stem.replace(
                "graph_response_",
                "",
            )

            with open(file_path, "r", encoding="utf-8") as file:
                graph_response = json.load(file)

            features = self.builder.build_response(graph_response)

            for feature in features:
                record = {
                    "case_id": case_id,
                    **feature,
                }

                records.append(record)

        dataset = pd.DataFrame(records)

        dataset = dataset.merge(
            labels,
            left_on=["case_id", "vasp_id"],
            right_on=["case_id", "candidate_vasp_id"],
            how="left",
        )

        dataset = dataset.drop(columns=["candidate_vasp_id"])

        return dataset

    def prepare_ml_data(self):
        """
        Load the dataset and prepare numeric features (X)
        and labels (y) for machine learning.
        """

        dataset = self.load()

        feature_columns = [
            "graph_distance",
            "path_strength",
            "transaction_count",
            "address_confidence",
        ]

        X = dataset[feature_columns].copy()
        y = dataset["label"].astype(int).copy()

        return X, y