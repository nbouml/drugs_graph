import pandas as pd


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


df = pd.read_csv('/home/noureddine/PycharmProjects/drugs_graph/tests/data/input1.csv', index_col=0)
# cols = ('scientific_title', 'date')
cols = ("a", "b")
a = check_for_matching_if_nan(df, ref_cols=cols)
print(a)
