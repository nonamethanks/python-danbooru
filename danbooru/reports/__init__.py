"""Defines the danbooru report models individually."""
from danbooru.reports.artist_version_report import DanbooruArtistVersionReport
from danbooru.reports.forum_post_report import DanbooruForumPostReport
from danbooru.reports.note_version_report import DanbooruNoteVersionReport
from danbooru.reports.post_appeal_report import DanbooruPostAppealReport
from danbooru.reports.post_report import DanbooruPostReport
from danbooru.reports.wiki_page_version_report import DanbooruWikiPageVersionReport

_report_models = [
    DanbooruArtistVersionReport,
    DanbooruForumPostReport,
    DanbooruNoteVersionReport,
    DanbooruPostAppealReport,
    DanbooruPostReport,
    DanbooruWikiPageVersionReport,
]
