"""Model definition for /bulk_update_requests."""

from danbooru.model import DanbooruInstancedModel
from danbooru.models.forum_post import DanbooruForumPost


class DanbooruBulkUpdateRequest(DanbooruInstancedModel):
    user_id: int
    script: str
    status: str
    approver_id: int | None
    forum_post_id: int | None  # jfmsu
    forum_topic_id: int | None  # jfmsu
    tags: list[str]

    forum_post: DanbooruForumPost | None = None
