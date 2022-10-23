# from typing import Union

import pandas as pd
from pathlib import Path

from conf.settings import log


def get_df(file_path: Path, kwarg: dict = None) -> pd.DataFrame:
    if kwarg is None:
        kwarg = {}
    if str(file_path).endswith('.csv'):
        log.info(f"reading {file_path}")
        return pd.read_csv(file_path, **kwarg)
    else:
        log.warning(f"cannot read the file {file_path}")


def check_for_matching_if_nan(data: pd.DataFrame, ref_cols: tuple = ('scientific_title', 'date')) -> pd.DataFrame:
    """
    this function checks the presence of nans in the index, and tries to update other lines under certain conditions.

    Parameters
    ----------
    data: pd.DataFrame
            data to check
    ref_cols: tuple
            list the reference columns

    Returns
    -------
    pd.DataFrame

    return of updated data if necessary.
    """
    ref_cols = list(ref_cols)
    nan_index = data.index.isna()
    # TODO: improvement: in case we have several nan in the index
    res = data.apply(lambda x: x == data.loc[nan_index], axis=1)
    res = res.apply(lambda x: x[ref_cols].sum(1))
    res = res.loc[~res.index.isna()]
    index_to_update = res[res == len(ref_cols)].dropna().index
    if len(index_to_update) == 0:
        return data
    df_w_nan = data.loc[nan_index]
    df_w_nan.index = index_to_update
    df_temp = data.copy()
    df_temp.loc[index_to_update] = df_temp.loc[index_to_update].fillna(df_w_nan)
    return df_temp.loc[~df_temp.index.isna()]


def convert_col_in_datetime(data: pd.DataFrame,
                            columns: tuple = None,
                            dateformat: str = None,
                            day_first: bool = False) -> pd.DataFrame:
    """
    convert column(s) of a dataframe from string to datetime.

    Parameters
    ----------
    data: pd.DataFrame
        input data
    columns: tuple
            columns to convert
    dateformat: str
            The string to parse time, e.g. "%d/%m/%Y". Note that "%f" will parse all the way up to nanoseconds.
    day_first:
            Specify a date parse order if arg is str or is list-like.
            If True, parses dates with the day first, e.g. "10/11/12" is parsed as 2012-11-10.

    Returns
    -------
    pd.DataFrame

    dataframe with the right format for the concerned columns
    """
    columns = list(columns)
    df = data.copy()
    if dateformat is not None:
        df[columns] = df[columns].apply(lambda x: pd.to_datetime(x, format=dateformat))
    elif day_first:
        df[columns] = df[columns].apply(lambda x: pd.to_datetime(x, dayfirst=True))
    else:
        df[columns] = pd.to_datetime(df[columns])

    return df
