from abc import abstractmethod
from contextlib import contextmanager
from typing import ContextManager, Callable, Union, Optional, Dict, Any, List


TError = Union[
    str,
    List[str],
    Dict[str, Any],
    'ValidationError',
]


class ValidationError(Exception):
    """
    TODO
    """

    def __init__(self, error: Optional[TError] = None):
        """
        :param error:
        """
        if isinstance(error, ValidationError):
            error = error.error
        self.error = error or {}

    def __str__(self):
        return str(self.error)

    # @abstractmethod
    # def __repr__(self):
    #     """
    #     :return:
    #     """
    #     return 'ValidationError'

    def __bool__(self) -> bool:
        """
        :return:
        """
        return bool(self.error)

    @abstractmethod
    def add(
            self,
            key: str,
            error: TError,
    ):
        """
        :param key:
        :param error:
        """
        # if isinstance()

        if isinstance(error, str):
            self.error.setdefault(key, []).append(error)
        elif isinstance(error, ValidationError):
            self.error[key] = error.error
        else:
            raise ValueError(f'Invalid type: {type(error)}')


# class ValidationError(Exception):
#     """
#     TODO
#     """
#
#     def __init__(self, errors: Optional[Dict[str, List[str]]] = None):
#         """
#         :param errors:
#         """
#         self.errors = errors or {}
#
#     def __str__(self):
#         return str(self.errors)
#
#     def __bool__(self) -> bool:
#         """
#         :return:
#         """
#         return bool(self.errors)
#
#     def add(
#             self,
#             key: str,
#             error: Union[str, 'ValidationError'],
#     ):
#         """
#         :param key:
#         :param error:
#         """
#         if isinstance(error, str):
#             self.errors.setdefault(key, []).append(error)
#         elif isinstance(error, ValidationError):
#             self.errors[key] = error
#         else:
#             raise ValueError(f'Invalid type: {type(error)}')


TValidator = Callable


class Validator(object):
    pass


# class ValidationErrorGroup(object):
#
#     def __init__(self):
#         self.errors = ValidationError()
#
#     def __enter__(self) -> ValidationError:
#         return self.errors
#
#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         if self.errors:
#             raise self.errors


@contextmanager
def collect_validation_errors() -> ContextManager[ValidationError]:
    """
    A decorator to accumulate errors.
    """
    errors = ValidationError()
    yield errors
    if errors:
        raise errors
