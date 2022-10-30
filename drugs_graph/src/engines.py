from pathlib import Path
from typing import Callable, Union

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
    global _engine
    if not _engine:
        if engine_type.lower() == 'memory':
            _engine = MemoryEngine()
    return _engine


def apply_operation(opera: Callable,
                    file_path_in: Union[Path, tuple],
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
        kwargs_get_df = {'index_col': 0}
    if kwargs_save_df is None:
        kwargs_save_df = {}

    log.info(f"applying {opera.__name__} operation on {file_path_in}")
    if isinstance(file_path_in, tuple):
        data_in = []
        if len(kwargs_get_df) == 1:
            kwargs_get_df = [kwargs_get_df] * len(file_path_in)
        for i, fp in enumerate(file_path_in):
            data_in += [ut.get_df(fp, kwargs_get_df[i])]
        data_in = tuple(data_in)
        res = opera(*data_in, *args_opera, **kwargs_opera)
    else:
        data_in = ut.get_df(file_path_in, kwargs_get_df)
        res = opera(data_in, *args_opera, **kwargs_opera)

    if file_path_out is not None:
        ut.save_df(res, file_path_out, kwargs_save_df)
    else:
        log.info(f"the result of {opera.__name__} method, will not be saved automatically")

    return res


class MemoryEngine:
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
        res = apply_operation(opera=opera,
                              file_path_in=file_path_in,
                              file_path_out=file_path_out,
                              args_opera=args_opera,
                              kwargs_opera=kwargs_opera,
                              kwargs_get_df=kwargs_get_df,
                              kwargs_save_df=kwargs_save_df)
        self._operations.append(res)
        self.data = res

        return self

    def result(self):
        return self.data

    def wait(self):
        pass


class OtherEngine:
    pass
