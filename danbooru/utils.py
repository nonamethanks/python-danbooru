"""Various utility methods are defined here."""

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel as _PydanticModel


class classproperty:
    def __init__(self, func: Callable):
        """Bring back class properties deprecated in 3.11."""
        self.fget = func

    def __get__(self, instance: Any, owner: Any):
        return self.fget(owner)


class BaseModel(_PydanticModel):
    class Config:
        ignored_types = (classproperty, )
        extra = "allow"
