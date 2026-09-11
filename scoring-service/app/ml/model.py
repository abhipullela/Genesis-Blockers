import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


FEATURE_COLUMNS = [
    "graph_distance",
    "path_strength",
    "transaction_count",
    "address_confidence",
]


class AttributionModel:
    def __init__(self, model_type: str = "logistic"):
        self.model_type = model_type

        if model_type == "logistic":
            self.model = LogisticRegression(
                random_state=42,
                max_iter=1000,
            )

        elif model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=5,
            )

        else:
            raise ValueError(
                f"Unsupported model type: {model_type}"
            )

    def train(self, dataset: pd.DataFrame) -> None:
        X = dataset[FEATURE_COLUMNS]
        y = dataset["label"].astype(int)

        self.model.fit(X, y)

    def predict_proba(
        self,
        dataset: pd.DataFrame,
    ) -> list[float]:
        X = dataset[FEATURE_COLUMNS]

        probabilities = self.model.predict_proba(X)

        return probabilities[:, 1].tolist()

    def predict(
        self,
        dataset: pd.DataFrame,
    ) -> list[int]:
        X = dataset[FEATURE_COLUMNS]

        return self.model.predict(X).tolist()