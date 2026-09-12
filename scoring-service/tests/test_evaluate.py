from app.features.dataset import DatasetLoader
from app.ml.evaluate import ModelEvaluator
from app.ml.split import DatasetSplitter


def test_model_evaluation():
    dataset = DatasetLoader().load()

    splitter = DatasetSplitter()
    train, test = splitter.split(dataset)

    evaluator = ModelEvaluator()

    results = evaluator.evaluate(
        train,
        test,
    )

    assert "baseline" in results
    assert "logistic_regression" in results

    for model_name in results:
        metrics = results[model_name]

        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["precision"] <= 1.0
        assert 0.0 <= metrics["recall"] <= 1.0
        assert 0.0 <= metrics["f1"] <= 1.0
        assert 0.0 <= metrics["roc_auc"] <= 1.0
        assert 0.0 <= metrics["pr_auc"] <= 1.0