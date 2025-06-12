"""Model definition for /reports/posts."""

from __future__ import annotations

import datetime

from danbooru.model import DanbooruModel


class DanbooruPostReport(DanbooruModel):
    date: datetime.datetime = None
    posts: int
