"""Model definition for /bulk_update_requests."""

from danbooru.model import DanbooruModel
from danbooru.models.forum_post import DanbooruForumPost


class DanbooruBulkUpdateRequest(DanbooruModel):
    user_id: int
    forum_topic_id: int
    script: str
    status: str
    approver_id: int | None
    forum_post_id: int | None
    tags: list[str]

    forum_post: DanbooruForumPost | None = None
