"""Model definition for /reports/posts."""

from __future__ import annotations

from danbooru.report_model import DanbooruReportModel


class DanbooruPostReport(DanbooruReportModel):
    posts: int
    uploader: str | None = None
