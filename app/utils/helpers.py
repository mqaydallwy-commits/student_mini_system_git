"""Small reusable formatting and collection helpers."""
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def format_record(label: str, *values: object, **details: object) -> str:
    """Format positional values and named details as one CLI record."""
    parts = [label, *(str(value) for value in values)]
    parts.extend(f"{key}={value}" for key, value in details.items())
    return " | ".join(parts)


def transform_records(items: Iterable[T], transform: Callable[[T], R]) -> list[R]:
    """Apply a caller-provided transformation to every item."""
    return list(map(transform, items))


def filter_records(items: Iterable[T], predicate: Callable[[T], bool]) -> list[T]:
    """Keep only items accepted by a caller-provided predicate."""
    return list(filter(predicate, items))
