"""User UserLevel helpers."""

from __future__ import annotations

from pydantic import model_serializer, model_validator

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
    def validate_model(cls, value: int | str | dict | UserLevel) -> dict:
        """Validate that the level is valid."""
        if isinstance(value, str):
            name = value.upper()
            number = cls.number_from_name(name)

        elif isinstance(value, int):
            number = value
            name = cls.name_from_number(number)

        elif isinstance(value, UserLevel):
            name = value.name
            number = value.number

        else:
            e = f"{value} ({type(value)}): not an acceptable value."
            raise TypeError(e)

        return {"number": number, "name": name}

    @model_serializer
    def serializer(self) -> int:
        """Serialize the level."""
        return self.number

    @staticmethod
    def name_from_number(number: int) -> str:
        """Return the level number from a name."""
        try:
            number_index = list(LEVEL_MAP.values()).index(number)
            name = list(LEVEL_MAP.keys())[number_index]
        except (IndexError, ValueError) as e:
            msg = f"No level with number {number}."
            raise ValueError(msg) from e
        else:
            return name

    @staticmethod
    def number_from_name(name: str) -> int:
        """Return the level name from a number."""
        try:
            number = LEVEL_MAP[name]
        except KeyError as e:
            msg = f"No level with name {name}."
            raise ValueError(msg) from e
        else:
            return number

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
