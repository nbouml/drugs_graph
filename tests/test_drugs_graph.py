import pandas as pd
from pathlib import Path
from src import utils
import pytest

DATA_FOLDER = Path(__file__, fs="local").parent / "data"
df_in1 = pd.read_csv(f"{DATA_FOLDER}/input1.csv", index_col=0)
df_out1 = pd.read_csv(f"{DATA_FOLDER}/output1.csv", index_col=0)


@pytest.mark.parametrize(
    "data_in, ref_cols, expected",
    (
            [df_in1, ("a", "b"), df_out1],
            [df_in1, ("a", "c"), df_in1],
    )
)
def test_check_for_matching_if_nan(data_in, ref_cols, expected):
    res = utils.check_for_matching_if_nan(data_in, ref_cols=ref_cols)
    pd.testing.assert_frame_equal(res, expected)
