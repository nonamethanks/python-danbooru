"""Model definition for /forum_posts."""

from danbooru.model import DanbooruInstancedModel


class DanbooruForumPost(DanbooruInstancedModel):
    creator_id: int
    body: str
    updater_id: int
    is_deleted: bool
    topic_id: int
