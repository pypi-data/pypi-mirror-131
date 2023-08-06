import datetime
import sys
import logging

sys.path.append('../')

LOGGER = logging.getLogger('client')

def logger(log_func):
    """
    A decorator that logs function calls.
    Saves debug events containing
    information about the name of the called function, the parameters with which
    the function is called, and the module is calling the function.
    :param log_func:
    :return:
    """
    def log_saver(*args, **kwargs):
        result = log_func(*args, **kwargs)
        LOGGER.debug(f'{datetime.datetime.now()}. Function {log_func.__name__} is called from module {log_func.__module__}', stacklevel=2)
        return result
    return log_saver

