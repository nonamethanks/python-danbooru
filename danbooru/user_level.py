"""User UserLevel helpers."""

from __future__ import annotations

from typing import ClassVar, overload


class UserLevel:
    LEVEL_MAP: ClassVar = {
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

    ANONYMOUS = LEVEL_MAP["ANONYMOUS"]
    RESTRICTED = LEVEL_MAP["RESTRICTED"]
    MEMBER = LEVEL_MAP["MEMBER"]
    GOLD = LEVEL_MAP["GOLD"]
    PLATINUM = LEVEL_MAP["PLATINUM"]
    BUILDER = LEVEL_MAP["BUILDER"]
    CONTRIBUTOR = LEVEL_MAP["CONTRIBUTOR"]
    APPROVER = LEVEL_MAP["APPROVER"]
    MODERATOR = LEVEL_MAP["MODERATOR"]
    ADMIN = LEVEL_MAP["ADMIN"]
    OWNER = LEVEL_MAP["OWNER"]

    @overload
    def __init__(self, *, name: str, number: None = None): ...
    @overload
    def __init__(self, *, name: None = None, number: int): ...

    def __init__(self, name: str | None = None, number: int | None = None):
        """Takes either the level name or number."""
        if name is None and number is None:
            e = "Only one of name, id_ can be provided."
            raise ValueError(e)

        if name:
            name = name.upper()
            try:
                number = self.LEVEL_MAP[name]
            except KeyError as e:
                e.add_note(f"No level with name {name}.")
                raise

        if number:
            try:
                number_index = list(self.LEVEL_MAP.values()).index(number)
                name = list(self.LEVEL_MAP.keys())[number_index]
            except (IndexError, ValueError) as e:
                e.add_note(f"No level with number {number}.")
                raise

        self.name: str = name
        self.number: int = number

    @staticmethod
    def get(value: str | int) -> UserLevel:
        """Get a level object from an unknown value."""
        level = UserLevel(
            name=value if isinstance(value, str) else None,
            number=value if isinstance(value, int) else None,
        )
        return level

    def __lt__(self, value: int | UserLevel | str) -> bool:
        return self.number < UserLevel.get(value).number

    def __gt__(self, value: int | UserLevel | str) -> bool:
        return self.number > UserLevel.get(value).number

    def __le__(self, value: int | UserLevel | str) -> bool:
        return self.number <= UserLevel.get(value).number

    def __ge__(self, value: int | UserLevel | str) -> bool:
        return self.number >= UserLevel.get(value).number

    def __repr__(self) -> str:
        return f"UserLevel<{self.name}>"
