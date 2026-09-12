from app.features.dataset import DatasetLoader


def test_dataset_loader():
    loader = DatasetLoader()

    dataset = loader.load()

    assert len(dataset) == 120
    assert dataset["case_id"].nunique() == 60
    assert dataset["label"].notna().all()

    assert "case_id" in dataset.columns
    assert "vasp_id" in dataset.columns
    assert "vasp_name" in dataset.columns
    assert "graph_distance" in dataset.columns
    assert "address_confidence" in dataset.columns
    assert "label" in dataset.columns

    assert dataset["label"].notna().all()


def test_prepare_ml_data():
    loader = DatasetLoader()

    X, y = loader.prepare_ml_data()

    assert len(X) == 120
    assert len(y) == 120

    assert list(X.columns) == [
        "graph_distance",
        "path_strength",
        "transaction_count",
        "address_confidence",
    ]

    assert X.dtypes.notna().all()
    assert y.dtype.kind in "iu"

    assert y.isin([0, 1]).all()