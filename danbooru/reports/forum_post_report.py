"""Model definition for /reports/forum_posts."""

from __future__ import annotations

from danbooru.report_model import DanbooruReportModel


class DanbooruForumPostReport(DanbooruReportModel):
    forum_posts: int
    creator: str | None = None
