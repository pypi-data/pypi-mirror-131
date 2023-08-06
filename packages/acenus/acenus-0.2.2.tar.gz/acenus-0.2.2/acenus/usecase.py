import functools
import logging
import inspect
import typing
import loguru

from acenus.executors_pool import ExecutorsPool


default_logger = loguru.logger


Logger = typing.Union[logging.Logger, logging.LoggerAdapter]


def get_func_kwargs(func: typing.Callable, kwargs: dict) -> dict:
    """ Inspect and get function kwargs """
    parameters = tuple(inspect.signature(func).parameters.keys())
    if "kwargs" not in parameters:
        kwargs = {k: v for k, v in kwargs.items() if k in parameters}
    return kwargs


def log_function(func: typing.Callable, logger: Logger):
    """ Decorator for log functions with exceptions """

    @functools.wraps(func)
    def _log_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            raise e
        else:
            logger.debug(
                f"Function {func.__name__} called",
                function=func.__name__,
                result=result,
                func_args=[str(arg) for arg in args],
                func_kwargs={k: str(v) for k, v in kwargs.items()},
            )
            return result

    return _log_function


Nothing = object()


def usecase(*funcs):
    """ Function composition with logging """
    funcs = list(funcs)

    def _usecase(
        data: typing.Any = Nothing, 
        executors_pool: typing.Optional[ExecutorsPool] = None,
        logger: typing.Optional[Logger] = default_logger,
    ):
        first_func = funcs[0]

        if logger: 
            first_func = log_function(first_func, logger)

        if data == Nothing:
            result = first_func()
        else:
            result = first_func(data)

        if executors_pool:
            result = executors_pool.execute(result)

        for func in funcs[1:]:
            if logger:
                func = log_function(func, logger)

            result = func(result)

            if executors_pool:
                result = executors_pool.execute(result)

        return result

    return _usecase
