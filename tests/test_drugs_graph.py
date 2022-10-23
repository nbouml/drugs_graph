import pandas as pd
from pathlib import Path
from src import utils
import pytest

DATA_FOLDER = Path(__file__, fs="local").parent / "data"
df_in1 = pd.read_csv(f"{DATA_FOLDER}/input1.csv", index_col=0)
df_out1 = pd.read_csv(f"{DATA_FOLDER}/output1.csv", index_col=0)
df_in2 = pd.read_csv(f"{DATA_FOLDER}/input2.csv", index_col=0)


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


@pytest.mark.parametrize(
    "path, kwargs, expected",
    (
            [Path(f"{DATA_FOLDER}/input1.csv"), {"index_col": 0}, df_in1],
    )
)
def test_get_df(path, kwargs, expected):
    res = utils.get_df(path, kwargs)
    pd.testing.assert_frame_equal(res, expected)


df_out2 = df_in2.copy()
df_out2['a'] = pd.to_datetime(df_out2['a'], dayfirst=True)
df_out3 = df_out2.copy()
df_out3['b'] = pd.to_datetime(df_out3['b'], dayfirst=True)
df_out4 = df_in2.copy()
df_out4['b'] = pd.to_datetime(df_out4['b'], format="%d/%m/%y")


@pytest.mark.parametrize(
    "data, columns, dateformat, day_first, expected",
    (
            [df_in2, ("a",), None, True, df_out2],
            [df_in2, ("a", "b"), None, True, df_out3],
            [df_in2, ("b",), "%d/%m/%y", False, df_out4]
    )
)
def test_convert_col_in_datetime(data, columns, dateformat, day_first, expected):
    # noinspection PyTypeChecker
    res = utils.convert_col_in_datetime(data=data, columns=columns, dateformat=dateformat, day_first=day_first)
    # noinspection PyTypeChecker
    pd.testing.assert_frame_equal(res, expected)
