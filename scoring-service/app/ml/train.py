from pathlib import Path

import joblib

from app.features.dataset import DatasetLoader
from app.ml.model import AttributionModel
from app.ml.split import DatasetSplitter


MODEL_PATH = Path("models/attribution_random_forest.joblib")


def train_and_save():
    loader = DatasetLoader()
    dataset = loader.load()

    splitter = DatasetSplitter()
    train_dataset, _ = splitter.split(dataset)

    model = AttributionModel("random_forest")
    model.train(train_dataset)

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model.model,
        MODEL_PATH,
    )

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save()