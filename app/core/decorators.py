"""Reusable decorators for service methods."""
import logging
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from app.core.exceptions import AuthenticationError

P = ParamSpec("P")
R = TypeVar("R")
logger = logging.getLogger(__name__)


def log_action(func: Callable[P, R]) -> Callable[P, R]:
    """Log a service action while preserving the wrapped function metadata."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info("Action: %s", func.__qualname__)
        return func(*args, **kwargs)

    return wrapper


def requires_auth(func: Callable[P, R]) -> Callable[P, R]:
    """Allow a service operation only when its authentication state is active."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not args or not bool(getattr(args[0], "is_authenticated", False)):
            raise AuthenticationError("Authentication required.")
        return func(*args, **kwargs)

    return wrapper
