"""Model definition for /reports/wiki_page_versions."""

from __future__ import annotations

from danbooru.report_model import DanbooruReportModel


class DanbooruWikiPageVersionReport(DanbooruReportModel):
    wiki_edits: int
    updater: str | None = None
