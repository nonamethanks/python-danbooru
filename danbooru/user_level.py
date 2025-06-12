"""User UserLevel helpers."""

from __future__ import annotations

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
    name: str
    number: int

    def __init__(self, value: str | int | UserLevel):
        """Takes either the level name or number."""
        if isinstance(value, str):
            name = value.upper()
            try:
                number = LEVEL_MAP[name]
            except KeyError as e:
                e.add_note(f"No level with name {name}.")
                raise

        elif isinstance(value, int):
            number = value
            try:
                number_index = list(LEVEL_MAP.values()).index(number)
                name = list(LEVEL_MAP.keys())[number_index]
            except (IndexError, ValueError) as e:
                e.add_note(f"No level with number {number}.")
                raise
        elif isinstance(value, UserLevel):
            name = value.name
            number = value.number

        super().__init__(name=name, number=number)

    def __lt__(self, value: int | UserLevel | str) -> bool:
        return self.number < UserLevel(value).number

    def __le__(self, value: int | UserLevel | str) -> bool:
        return self.number <= UserLevel(value).number

    def __gt__(self, value: int | UserLevel | str) -> bool:
        return self.number > UserLevel(value).number

    def __ge__(self, value: int | UserLevel | str) -> bool:
        return self.number >= UserLevel(value).number

    def __eq__(self, value: int | UserLevel | str) -> bool:
        return self.number == UserLevel(value).number

    def __repr__(self) -> str:
        return f"UserLevel<{self.name}>"
