from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from typing import get_origin, get_args
import inspect


__all__ = ["ValidationError", "ValidatorMixin", "ToDictMixin"]

EXCLUDE_PROPERTIES = ("parent", "children")


class ValidationError(AssertionError):
    pass


class ValidatorMixin:
    """A mixin to validate a model after initialization."""

    def validate(self):
        this_class = self.__class__.__name__
        assert is_dataclass(self), f"{this_class} should be a dataclass"

        validation_errors = list(
            self.validation_generator(self, type(self), this_class)
        )
        message = "\n - ".join(validation_errors)
        if message:
            raise ValidationError(f"invalid fields in {this_class}:\n - {message}\n")

    def validation_generator(self, item, type_=None, name=""):
        if is_dataclass(item):
            for field in fields(item):
                if field.init:
                    errors = self._validate_item(
                        getattr(item, field.name), field.type, field.name
                    )
                    for validation_error in errors:
                        yield validation_error
        else:
            for validation_error in self._validate_item(item, type_, name):
                yield validation_error

    def _validate_container(self, container, type_, name):
        if isinstance(container, (list, tuple, set)):
            for item in container:
                for validation_error in self.validation_generator(
                    item, get_args(type_)[0], name
                ):
                    yield validation_error
        elif isinstance(container, Mapping):
            for item in container.values():
                for validation_error in self.validation_generator(
                    item, get_args(type_)[1], name
                ):
                    yield validation_error

    def _validate_item(self, item, type_, name):
        if item is not self:
            origin = get_origin(type_)
            args = get_args(type_)
            if origin is not None:
                try:
                    if not isinstance(item, origin):
                        yield f"{name}: {item} {origin} is not of type {type_}"
                except TypeError:
                    if not isinstance(item, args):
                        yield f"{name}: {item} {origin}[{args}] is not of type {type_}"
                for validation_error in self._validate_container(item, type_, name):
                    yield validation_error
            else:
                if not isinstance(item, type_):
                    yield f"{name}: {item} {type(item)} is not of type {type_}"


class ToDictMixin:
    """A mixin to validate a model after initialization."""

    def to_dict(self, obj=None):
        if obj is None:
            obj = self
        if is_dataclass(obj):
            return dict(
                **{
                    field_.name: self.to_dict(getattr(obj, field_.name))
                    for field_ in fields(obj)
                    if field_.init and field_.repr
                },
                **{
                    p: self.to_dict(getattr(obj, p))
                    for p in self.properties(obj, EXCLUDE_PROPERTIES)
                },
            )
        if isinstance(obj, (str, float, int, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            return {k: self.to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, "__iter__") and callable(obj.__iter__):
            return [self.to_dict(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            return {
                k: self.to_dict(v)
                for k, v in obj.__dict__.items()
                if k not in ["__module__", "__dict__", "__weakref__", "__doc__"]
            }
        else:
            return repr(obj)

    def properties(self, obj, exclude=()):
        return [
            attr
            for attr in dir(obj)
            if self.is_property(obj, attr)
            and attr not in exclude
            and not attr.startswith("_")
        ]

    @staticmethod
    def is_property(obj, attr):
        return isinstance(inspect.getattr_static(obj, attr), property)
