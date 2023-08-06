from types import SimpleNamespace
from typing import Callable, Optional, Dict, Any, NamedTuple

from .validation import ValidationError


# Unless otherwise specified, fields will be deserialized into a
# SimpleNamespace, as its constructor takes **kwargs, which are available
# afterwards as attributes on the object (similar to how dataclasses works).
default_factory = SimpleNamespace
# default_factory = NamedTuple  # TODO


class Context(object):
    """
    The context implements and describes a common set of options
    used when serializing and deserializing.
    """

    def __init__(
            self,
            options: Optional[Dict[Any, Any]] = None,
            include_none: bool = True,
            strict: bool = True,
            ordered: bool = False,
            default_factory: Callable = default_factory,
            default_date_format: str = '',  # TODO
            default_time_format: str = '',  # TODO
            default_datetime_format: str = '',  # TODO
    ):
        """
        :param options: Arbitrary dict to store custom options.
            Accessible by Schema and Field when serializing and deserializing.
        :param include_none: Whether to include None values when serializing.
        :param ordered: Whether to keep the order of keys when serializing.
        :param strict: Default strict for Schemas, unless
        :param ordered:
        :param default_factory:
        :param default_date_format:
        :param default_time_format:
        :param default_datetime_format:
        """
        self.options = options or {}
        self.include_none = include_none
        self.ordered = ordered
        self.default_factory = default_factory
        self.default_date_format = default_date_format
        self.default_time_format = default_time_format
        self.default_datetime_format = default_datetime_format

    def create_validation_error(self) -> ValidationError:
        """
        Creates a new, empty instance of ValidationError.

        If replacing the default ValidationError class, make sure you return
        a type that is a subclass of ValidationError.
        """
        return ValidationError()


# -- Singletons --------------------------------------------------------------

default_context = Context()
