"""Defines the danbooru models individually."""

from danbooru.models.artist_version import DanbooruArtistVersion
from danbooru.models.bulk_update_request import DanbooruBulkUpdateRequest
from danbooru.models.comment import DanbooruComment
from danbooru.models.comment_vote import DanbooruCommentVote
from danbooru.models.forum_post import DanbooruForumPost
from danbooru.models.post import DanbooruPost
from danbooru.models.post_counts import DanbooruPostCounts
from danbooru.models.post_version import DanbooruPostVersion
from danbooru.models.post_vote import DanbooruPostVote
from danbooru.models.related_tag import DanbooruRelatedTag
from danbooru.models.tag import DanbooruTag
from danbooru.models.tag_implication import DanbooruTagImplication
from danbooru.models.user import DanbooruUser
from danbooru.models.wiki_page import DanbooruWikiPage
from danbooru.models.wiki_page_version import DanbooruWikiPageVersion

_models = [
    DanbooruArtistVersion,
    DanbooruBulkUpdateRequest,
    DanbooruComment,
    DanbooruCommentVote,
    DanbooruForumPost,
    DanbooruPost,
    DanbooruPostCounts,
    DanbooruPostVersion,
    DanbooruPostVote,
    DanbooruRelatedTag,
    DanbooruTag,
    DanbooruTagImplication,
    DanbooruUser,
    DanbooruWikiPage,
    DanbooruWikiPageVersion,
]
