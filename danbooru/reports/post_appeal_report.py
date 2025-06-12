"""Model definition for /reports/post_appeals."""

from __future__ import annotations

from danbooru.report_model import DanbooruReportModel


class DanbooruPostAppealReport(DanbooruReportModel):
    appeals: int
    creator: str | None = None
