"""User UserLevel helpers."""

from __future__ import annotations

from pydantic import model_validator

from danbooru.utils import BaseModel

LEVEL_MAP = {
    "ANONYMOUS": 0,
    "RESTRICTED": 10,
    "MEMBER": 20,
    "GOLD": 30,
    "PLATINUM": 31,
    "BUILDER": 32,
    "CONTRIBUTOR": 35,
    "APPROVER": 37,
    "MODERATOR": 40,
    "ADMIN": 50,
    "OWNER": 60,
}


class UserLevel(BaseModel):
    number: int
    name: str

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, value: int | str | UserLevel) -> dict:
        """Validate that the level is valid."""
        if isinstance(value, str):
            name = value.upper()
            try:
                number = LEVEL_MAP[name]
            except KeyError as e:
                msg = f"No level with name {name}."
                raise ValueError(e) from e

        elif isinstance(value, int):
            number = value
            try:
                number_index = list(LEVEL_MAP.values()).index(number)
                name = list(LEVEL_MAP.keys())[number_index]
            except (IndexError, ValueError) as e:
                msg = f"No level with number {number}."
                raise ValueError(msg) from e
        elif isinstance(value, UserLevel):
            name = value.name
            number = value.number
        else:
            e = f"{type(value)}: not an acceptable value."
            raise TypeError(e)

        return {"number": number, "name": name}

    def __lt__(self, level: int | UserLevel | str) -> bool:
        return self.number < UserLevel(level).number

    def __le__(self, level: int | UserLevel | str) -> bool:
        return self.number <= UserLevel(level).number

    def __gt__(self, level: int | UserLevel | str) -> bool:
        return self.number > UserLevel(level).number

    def __ge__(self, level: int | UserLevel | str) -> bool:
        return self.number >= UserLevel(level).number

    def __eq__(self, level: int | UserLevel | str) -> bool:
        return self.number == UserLevel(level).number

    def __repr__(self) -> str:
        return f"UserLevel<{self.name}>"
