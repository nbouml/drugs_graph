from pathlib import Path
from typing import Callable

from drugs_graph.src import utils as ut


def apply_operation(opera: Callable,
                    file_path_in: Path,
                    file_path_out: Path,
                    args_opera: dict = None,
                    kwargs_opera: dict = None,
                    kwargs_get_df: dict = None,
                    kwargs_save_df: dict = None):
    """
    Apply an operation on a file located in path_file_in and save the result in path_file_out

    Parameters
    ----------
    opera: Callable
            method to apply
    file_path_in: Path.
                Path of the input file
    file_path_out: Path.
                Path of the output result
    args_opera: dict
                args for operation
    kwargs_opera: dict
                kwargs for operation
    kwargs_get_df: dict
                kwargs for get_df function
    kwargs_save_df: dict
                kwargs for save_df function

    Returns
    -------
    Any

    return the result of the operation

    """
    if args_opera is None:
        args_opera = {}
    if kwargs_opera is None:
        kwargs_opera = {}
    if kwargs_get_df is None:
        kwargs_get_df = {}
    if kwargs_save_df is None:
        kwargs_save_df = {}

    data_in = ut.get_df(file_path_in, kwargs_get_df)
    res = opera(data_in, *args_opera, **kwargs_opera)
    ut.save_df(res, file_path_out, kwargs_save_df)

    return res


class MemoryEngine:
    def __init__(self):
        self._operations = []
        self.data = None

    def submit(self, operator, data, args):
        args = self.get_args(args)
        data = self.get_data(data)
        res = operator(*data, **args)
        self._operations.append(res)
        self.data = res
        return self

    @staticmethod
    def get_args(args):
        return args

    @staticmethod
    def get_data(data):
        return data

    def result(self):
        return self.data

    def wait(self):
        pass


class OtherEngine:
    pass
