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

    def __init__(self, level: int | str | UserLevel | None = None, **data):  # noqa: D107
        if level is not None:
            super().__init__(level=level)
        else:
            super().__init__(**data)

    @model_serializer
    def serializer(self) -> int:
        """Serialize the level as an int for DB and Peewee. Accepts both UserLevel and int."""
        # If self is already an int (shouldn't happen, but for robustness)
        if isinstance(self, int):
            return self
        # Normal case: UserLevel instance
        return self.number

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, level: int | str | dict | UserLevel) -> dict:
        """Validate that the level is valid."""
        # Accept dicts with "number" and "name" keys (from model_dump)
        if isinstance(level, dict):
            if "number" in level and "name" in level:
                return {"number": level["number"], "name": level["name"]}
            if "level" in level:
                level = level["level"]
            else:
                e = f"{level} ({type(level)}): not an acceptable value."
                raise TypeError(e)

        # Accept int directly
        if isinstance(level, int):
            number = level
            name = cls.name_from_number(number)
            return {"number": number, "name": name}

        # Accept str directly
        if isinstance(level, str):
            name = level.upper()
            number = cls.number_from_name(name)
            return {"number": number, "name": name}

        # Accept UserLevel directly
        if isinstance(level, UserLevel):
            return {"number": level.number, "name": level.name}

        e = f"{level} ({type(level)}): not an acceptable value."
        raise TypeError(e)

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
        name = name.upper()
        if name == "MOD":
            name = "MODERATOR"
        elif name == "CONTRIB":
            name = "CONTRIBUTOR"

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
        return self.number == UserLevel(level=level).number

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self) -> str:
        return f"UserLevel[{self.name}]"
