"""Model definition for /reports/note_versions."""

from __future__ import annotations

from danbooru.report_model import DanbooruReportModel


class DanbooruNoteVersionReport(DanbooruReportModel):
    note_edits: int
    updater: str | None = None
