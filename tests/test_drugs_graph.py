import os
from typing import Union, Callable

import numpy as np
import pandas as pd
from pathlib import Path
from drugs_graph.src import utils, engines
# noinspection PyPackageRequirements
import pytest


DATA_FOLDER = Path(__file__, fs="local").parent / "data"
df_in1 = pd.read_csv(f"{DATA_FOLDER}/input1.csv", index_col=0)
df_out1 = pd.read_csv(f"{DATA_FOLDER}/output1.csv", index_col=0)
df_in2 = pd.read_csv(f"{DATA_FOLDER}/input2.csv", index_col=0)
df_in3 = pd.read_csv(f"{DATA_FOLDER}/input3.csv", index_col=0)
df_out2 = df_in2.copy()
df_out2['a'] = pd.to_datetime(df_out2['a'], dayfirst=True)
df_out3 = df_out2.copy()
df_out3['b'] = pd.to_datetime(df_out3['b'], dayfirst=True)
df_out4 = df_in2.copy()
df_out4['b'] = pd.to_datetime(df_out4['b'], format="%d/%m/%y")


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


@pytest.mark.parametrize(
    "path, kwargs, expected",
    (
            [Path(f"{DATA_FOLDER}/temp.csv"), {}, df_out1],
    )
)
def test_save_df(path, kwargs, expected):
    utils.save_df(expected, path, kwargs)
    res = utils.get_df(path, {'index_col': 0})
    pd.testing.assert_frame_equal(res, expected)
    os.remove(path)


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


@pytest.mark.parametrize(
    "file_path, kwarg, expected",
    (
            [f"{DATA_FOLDER}/input1.csv", {'index_col': 0}, df_in1],
            ["files/data.csv", None, None],
    )
)
def test_get_df(file_path: Path, kwarg: dict, expected: Union[pd.DataFrame, None]):
    file_path = Path(file_path)
    res = utils.get_df(file_path, kwarg)
    if expected is None:
        assert expected == res
        return
    pd.testing.assert_frame_equal(res, expected)


@pytest.mark.parametrize(
    "str_target, df_to_sniff, column_to_sniff, expected",
    (
            ['text1', df_out1, 'a', pd.Index(['id1'])],
            ['what', df_out1, 'b', pd.Index([])],
            ['AAAj55!!', df_out1, 'b', pd.Index([])]
    )
)
def test_str_sniffer(str_target: str, df_to_sniff: pd.DataFrame,
                     column_to_sniff: str,
                     expected: pd.Index):
    res = utils.str_sniffer(str_target, df_to_sniff, column_to_sniff)
    expected = expected.to_list()
    res = res.to_list()
    assert res == expected


@pytest.mark.parametrize(
    "opera, file_path_in, file_path_out, args_opera, kwargs_opera, kwargs_get_df, kwargs_save_df, expected",
    (
            [
                np.sum,
                DATA_FOLDER / "input3.csv",
                DATA_FOLDER / "temp3.csv",
                None,
                None,
                {"index_col": 0},
                None,
                1085

             ],
    )
)
def test_apply_operation(opera: Callable, file_path_in, file_path_out, args_opera,
                         kwargs_opera, kwargs_get_df, kwargs_save_df, expected: int):
    res = engines.apply_operation(opera, file_path_in, file_path_out, args_opera,
                                  kwargs_opera, kwargs_get_df, kwargs_save_df,)
    assert sum(res) == expected


@pytest.mark.parametrize(
    "df1, df2, cols_comm, index_col, expected",
    (
            [df_in3, df_in3, ('a', 'b'), 'a', df_in3],
    )
)
def test_concat_cols_from_dfs(df1, df2, cols_comm, index_col, expected):
    res = utils.concat_cols_from_dfs(df1, df2, cols_comm, index_col)
    pd.testing.assert_frame_equal(res, expected.set_index('a'))
