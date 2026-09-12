from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetSplitter:
    """
    Splits investigation cases into training and test sets.

    Candidates from the same investigation case always remain
    in the same split to prevent data leakage.
    """

    def split(
        self,
        dataset: pd.DataFrame,
        test_size: float = 0.25,
        random_state: int = 42,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:

        case_ids = dataset["case_id"].unique()

        train_cases, test_cases = train_test_split(
            case_ids,
            test_size=test_size,
            random_state=random_state,
        )

        train_dataset = dataset[
            dataset["case_id"].isin(train_cases)
        ].copy()

        test_dataset = dataset[
            dataset["case_id"].isin(test_cases)
        ].copy()

        return train_dataset, test_dataset