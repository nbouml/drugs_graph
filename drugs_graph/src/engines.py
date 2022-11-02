from pathlib import Path
from typing import Callable, Union, Tuple

import pandas as pd

from drugs_graph.src import utils as ut
from drugs_graph.conf.settings import engine_type
import logging
from drugs_graph.set_logging import setup_logger

logfile = "drugs_graph.log"
log = 'engines'
setup_logger(log, logfile, logging.DEBUG)
log = logging.getLogger(log)

_engine = None


def get_engine():
    """
    return the engine that will be used.
    To change the engine you can do it in .env by modifying settings.engine_type

    Returns
    -------

    object engine
    """
    global _engine
    if not _engine:
        if engine_type.lower() == 'memory':
            _engine = MemoryEngine()
    return _engine


def apply_operation(opera: Callable,
                    input_any: Union[Path, Tuple[Path], pd.DataFrame, Tuple[pd.DataFrame]],
                    file_path_out: Path = None,
                    args_opera: dict = None,
                    kwargs_opera: dict = None,
                    kwargs_get_df: Union[dict, tuple] = None,
                    kwargs_save_df: dict = None):
    """
    Apply an operation on a file located in path_file_in and save the result in path_file_out

    Parameters
    ----------
    opera: Callable
            method to apply
    input_any: Path(s), or Df(s)
            The Path(s) or Df(s) of the input data
    file_path_out: Path
            The Path of the output result
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
        kwargs_get_df = {'index_col': 0}
    if kwargs_save_df is None:
        kwargs_save_df = {}

    log.info(f"applying {opera.__name__} operation")
    if isinstance(input_any, tuple):
        data_in = []
        if len(kwargs_get_df) == 1:
            kwargs_get_df = [kwargs_get_df] * len(input_any)
        for i, fp in enumerate(input_any):
            if isinstance(fp, Path):
                data_in += [ut.get_df(fp, kwargs_get_df[i])]
            else:
                data_in += [input_any[i]]
        data_in = tuple(data_in)
        res = opera(*data_in, *args_opera, **kwargs_opera)
    else:
        if isinstance(input_any, Path):
            data_in = ut.get_df(input_any, kwargs_get_df)
        else:
            data_in = input_any.copy()
        res = opera(data_in, *args_opera, **kwargs_opera)

    if file_path_out is not None:
        ut.save_df(res, file_path_out, kwargs_save_df)
    else:
        log.info(f"the result of {opera.__name__} method, will not be saved automatically")

    return res


class MemoryEngine:
    """
    This engine will perform the calculation in memory and sequentially.
    """
    def __init__(self):
        self._operations = []
        self.data = None

    def submit(self, opera: Callable,
               file_path_in: Path,
               file_path_out: Path = None,
               args_opera: dict = None,
               kwargs_opera: dict = None,
               kwargs_get_df: dict = None,
               kwargs_save_df: dict = None):
        """
        This method will submit a job to apply_operation

        Parameters
        ----------
        opera: Callable
                method to apply
        file_path_in: Path
                The Path of the input file
        file_path_out: Path
                The Path of the output result
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
        MemoryEngine

        """
        res = apply_operation(opera=opera, input_any=file_path_in, file_path_out=file_path_out, args_opera=args_opera,
                              kwargs_opera=kwargs_opera, kwargs_get_df=kwargs_get_df, kwargs_save_df=kwargs_save_df)
        self._operations.append(res)
        self.data = res

        return self

    def result(self):
        """
        Get the result

        Returns
        -------
        self.data

        """
        return self.data

    def wait(self):
        """
        Wait method

        Returns
        -------

        """
        pass


class OtherEngine:
    """
    You can implement other engines.
    """
    pass
