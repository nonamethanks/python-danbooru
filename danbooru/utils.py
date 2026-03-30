"""Various utility methods are defined here."""

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel as _PydanticModel
from pydantic import ValidationError


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

    def __init__(self, **data):
        """Try to intercept eventual errors and print the whole thing for easier debugging."""
        try:
            super().__init__(**data)
        except ValidationError as e:
            try:
                values = value_from_validation_error(data, e)
            except KeyError:
                e.add_note(f"Failed to validate the following input:\n>\t{data}\n")
            else:
                e.add_note(f"\n>\t{data}\nFailed to validate the following input:\n>\t{values}\n")
            raise
        else:
            self._raw_data = data


def value_from_validation_error(data: dict, exception: ValidationError) -> dict:
    """Extract the values from the validation error."""
    values = {}
    for error in exception.errors():
        loc = error["loc"]
        value = data
        for field in loc:
            if field == "__root__":
                break
            value = value[field]
        values[".".join([str(location) for location in loc])] = value
    return values
