from app.features.dataset import DatasetLoader
from app.ml.model import AttributionModel


def test_model_training():
    dataset = DatasetLoader().load()

    train_dataset = dataset[
        dataset["case_id"].isin(
            [
                "003",
                "004",
                "005",
                "006",
                "007",
                "008",
                "010",
                "011",
                "012",
                "013",
                "014",
                "015",
                "017",
                "019",
                "020",
            ]
        )
    ]

    model = AttributionModel()
    model.train(train_dataset)

    probabilities = model.predict_proba(train_dataset)
    predictions = model.predict(train_dataset)

    assert len(probabilities) == len(train_dataset)
    assert len(predictions) == len(train_dataset)

    assert all(
        0.0 <= probability <= 1.0
        for probability in probabilities
    )

    assert all(
        prediction in [0, 1]
        for prediction in predictions
    )