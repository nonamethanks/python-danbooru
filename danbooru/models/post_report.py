"""Model definition for /reports/posts."""

from __future__ import annotations

import datetime

from danbooru.model import DanbooruModel


class DanbooruPostReport(DanbooruModel):
    date: datetime.datetime = None
    posts: int

    def __repr__(self) -> str:
        props = " ".join(f"{k}={v}" for k, v in self.model_dump(exclude_none=True).items())
        return f"{type(self).__name__}<{props}>"
