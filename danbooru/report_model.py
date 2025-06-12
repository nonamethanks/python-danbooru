"""Model definition for reports."""

from __future__ import annotations

import datetime

from danbooru.model import DanbooruModel
from danbooru.user_level import UserLevel


class DanbooruReportModel(DanbooruModel):
    date: datetime.datetime = None
    level: UserLevel | None = None

    def __repr__(self) -> str:
        props = " ".join(f"{k}={v}" for k, v in self.model_dump(exclude_none=True).items())
        return f"{type(self).__name__}<{props}>"
