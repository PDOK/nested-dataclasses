"""
Implements decorator `nested` that adds a parent and children to a dataclass.

Both parent and child class should be decorated with nested.

Usage:

Example usage of the parent attribute on a nested dataclass:
```
from dataclasses import dataclass
from typing import List

from nested_dataclasses import nested


@nested
@dataclass
class TextCount:
    text: str
    count: int

    @property
    def fraction(self):
        return self.count / self.parent.total_count

@nested
@dataclass
class TextCounts:
    counts: List[TextCount]

    @property
    def total_count(self):
        return sum(count.count for count in self.counts)

hello = TextCount("hello", 3)
hi = TextCount("hi", 1)
counts = TextCounts([hello, hi])

counts.validate()

print(counts.counts[0].fraction)
print(counts.children)
print(counts.to_dict())
```
"""
from nested_dataclasses.nested_dataclass import nested
from nested_dataclasses.mixins import ValidationError, ValidatorMixin, ToDictMixin

__all__ = [nested, ValidationError, ValidatorMixin, ToDictMixin]
