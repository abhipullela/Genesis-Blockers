from app.features.dataset import DatasetLoader
from app.ml.split import DatasetSplitter


def test_case_aware_split():
    dataset = DatasetLoader().load()

    splitter = DatasetSplitter()

    train, test = splitter.split(dataset)

    train_cases = set(train["case_id"])
    test_cases = set(test["case_id"])

    assert len(train) > 0
    assert len(test) > 0

    assert train_cases.isdisjoint(test_cases)

    assert len(train_cases) + len(test_cases) == 60