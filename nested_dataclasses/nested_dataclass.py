from dataclasses import dataclass, field, fields
from typing import List, Mapping, Sequence

from nested_dataclasses.mixins import ValidatorMixin, ToDictMixin

__all__ = ["nested"]


@dataclass(repr=False)
class ParentDataclass:
    __children: List[str] = field(repr=False, init=False, compare=False)

    def __post_init__(self):
        self.__update_children__()

    def __update_children__(self):
        self.__children = []
        for field_ in fields(self):
            if field_.init:
                item = getattr(self, field_.name, None)
                if isinstance(item, Sequence):
                    for subitem in item:
                        if issubclass(subitem.__class__, NestedDataclass):
                            subitem.parent = self
                            self.__children.append(field_.name)
                elif issubclass(item.__class__, NestedDataclass):
                    item.parent = self
                elif isinstance(item, Mapping):
                    for subitem in item.values():
                        if issubclass(subitem.__class__, NestedDataclass):
                            subitem.parent = self
                            self.__children.append(field_.name)

    @property
    def children(self):
        try:
            return [getattr(self, c) for c in self.__children]
        except AttributeError:
            return []


@dataclass(repr=False)
class NestedDataclass(ParentDataclass):
    _parent: ParentDataclass = field(repr=False, init=False, compare=False)
    # parent: Optional[ParentDataclass] = field(repr=False, init=False, compare=False)

    @property
    def parent(self):
        try:
            return self._parent
        except AttributeError:
            return None  # Explicit, not a child

    @parent.setter
    def parent(self, var):
        if issubclass(var.__class__, ParentDataclass) and not hasattr(self, "_parent"):
            self._parent = var


def nested_base(cls, validator, to_dict):
    classes = [
        NestedDataclass,
    ]
    if validator:
        classes.append(ValidatorMixin)
    if to_dict:
        classes.append(ToDictMixin)

    @dataclass(repr=False)
    class Nested(cls, *classes):
        __module__ = cls.__module__
        __name__ = cls.__name__
        __doc__ = cls.__doc__

        def __repr__(self):
            fs = [(f.name, getattr(self, f.name, None)) for f in fields(self) if f.repr]
            s = ", ".join(f"{name}={val}" for name, val in fs if val is not None)
            return f"{self.__name__}({s})"

    return Nested


def nested(cls=None, /, *, validator=True, to_dict=True):
    def wrap(klass):
        return nested_base(klass, validator, to_dict)

    # See if we're being called as @nested or @nested().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @nested without parens.
    return wrap(cls)
