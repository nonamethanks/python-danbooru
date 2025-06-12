"""Model definition for /reports/posts."""

from __future__ import annotations

import datetime

from danbooru.model import DanbooruModel
from danbooru.user_level import UserLevel


class DanbooruPostReport(DanbooruModel):
    date: datetime.datetime = None
    posts: int

    level: UserLevel | None = None

    def __repr__(self) -> str:
        props = " ".join(f"{k}={v}" for k, v in self.model_dump(exclude_none=True).items())
        return f"{type(self).__name__}<{props}>"
