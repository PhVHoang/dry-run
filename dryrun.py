from collections import defaultdict, OrderedDict
from functools import wraps
import inspect

from utils import logger
from utils.constants import DRY_RUN_FUNCTION_KWARGS
from utils.exceptions import DruRunFunctionNotDefined

_LOGGER = logger.log("dry_run")


def get_signatures(func):
    """Get signatures of a function.

    :param func: function
    :return: signatures of this function
    """
    params = inspect.signature(func).parameters
    args = []
    kwargs = OrderedDict()
    for p in params.values():
        if p.default is p.empty:
            args.append(p.name)
        else:
            kwargs[p.name] = p.default
    return args, kwargs


class DryRun:
    _dry_run = defaultdict(lambda: False)

    def __init__(self, value=None, *, label='default'):
        self._value = value
        self._label = label

    @classmethod
    def set(cls, value, label='default'):
        if value:
            cls._dry_run[label] = True
        else:
            cls._dry_run[label] = False

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._dry_run[self._label]:
                args_string = ', '.join([str(argument) for argument in args])
                kwargs_string = ', '.join(['{}={}'.format(key, value) for (key, value) in kwargs.items()])
                if len(kwargs) > 0:
                    if len(args) > 0:
                        kwargs_string = ', {}'.format(kwargs_string)
                _LOGGER.logger.info(
                    'dryrun[{label}] skip: {function}( {args}{kwargs} )'.format(
                        label=self._label, function=func.__qualname__, args=args_string, kwargs=kwargs_string
                    )
                )
                _, func_kwargs = get_signatures(func)
                if DRY_RUN_FUNCTION_KWARGS not in func_kwargs:
                    _LOGGER.logger.error(
                        f'Missing argument: dry_run_function on {func.__qualname__}'
                    )
                    raise DruRunFunctionNotDefined('Missing argument: dry_run_function')
                return func_kwargs.get(DRY_RUN_FUNCTION_KWARGS)(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper


set = DryRun.set
