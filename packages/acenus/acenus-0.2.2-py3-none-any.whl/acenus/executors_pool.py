import typing
import logging


default_logger = logging.getLogger()


Logger = typing.Union[logging.Logger, logging.LoggerAdapter]


class ExecutorsPool:

    def __init__(
        self,
        executors: typing.Optional[list] = None,
        logger: Logger = default_logger,
    ):
        self._executors = executors or list()
        self.logger = logger

    def add(
        self,
        type_: typing.Type,
        executor: typing.Callable,
        *args,
        **kwargs,
    ) -> None:
        self._executors.append({
            'type': type_,
            'executor': executor,
            'args': args or list(),
            'kwargs': kwargs or dict(),
        })

    def remove(self, type_: typing.Type) -> None:
        self._executors = [
            executor
            for executor in self._executors
            if executor['type'] != type_
        ]

    def execute(self, data: typing.Any) -> typing.Any:
        for executor_data in self._executors:
            if isinstance(data, executor_data['type']):
                result = executor_data['executor'](
                    data,
                    *executor_data['args'],
                    **executor_data['kwargs'],
                )
                self.logger.debug(
                    f'Executor for {type(data)} executed', 
                    extra=dict(
                        data=data,
                        type=executor_data['type'],
                        executor=executor_data['type'].__name__,
                        func_args=[str(arg) for arg in executor_data['args']],
                        func_kwargs={
                            k: str(v) 
                            for k, v in executor_data['kwargs'].items()
                        },
                        result=result,
                    )
                )
                return result

        self.logger.debug(f'No executors for {type(data)}. Return raw')
        return data
