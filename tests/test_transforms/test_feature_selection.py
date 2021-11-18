import pandas as pd
import pytest

from etna.datasets import TSDataset
from etna.datasets import generate_ar_df
from etna.transforms.feature_selection import BaseFeatureSelectionTransform


@pytest.fixture
def ts_with_complex_exog(random_seed) -> TSDataset:
    df = generate_ar_df(periods=100, start_time="2020-01-01", n_segments=4)

    df_exog_1 = generate_ar_df(periods=100, start_time="2020-01-01", n_segments=4, random_seed=2).rename(
        {"target": "exog"}, axis=1
    )
    df_exog_2 = generate_ar_df(periods=150, start_time="2019-12-01", n_segments=4, random_seed=3).rename(
        {"target": "regressor_1"}, axis=1
    )
    df_exog_3 = generate_ar_df(periods=150, start_time="2019-12-01", n_segments=4, random_seed=4).rename(
        {"target": "regressor_2"}, axis=1
    )

    df_exog = pd.merge(df_exog_1, df_exog_2, on=["timestamp", "segment"], how="right")
    df_exog = pd.merge(df_exog, df_exog_3, on=["timestamp", "segment"])

    df = TSDataset.to_dataset(df)
    df_exog = TSDataset.to_dataset(df_exog)
    ts = TSDataset(df=df, freq="D", df_exog=df_exog)
    return ts


def test_get_regressors(ts_with_complex_exog: TSDataset):
    regressors = BaseFeatureSelectionTransform._get_regressors(ts_with_complex_exog.df)
    assert sorted(regressors) == ["regressor_1", "regressor_2"]
