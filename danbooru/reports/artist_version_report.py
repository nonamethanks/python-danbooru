"""Model definition for /reports/artist_versions."""

from __future__ import annotations

from danbooru.report_model import DanbooruReportModel


class DanbooruArtistVersionReport(DanbooruReportModel):
    artist_edits: int
    updater: str | None = None
