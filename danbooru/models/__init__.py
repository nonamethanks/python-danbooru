"""Defines the danbooru models individually."""

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

_models = [
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
]
