"""Model definition for /tag_implications."""

from danbooru.model import DanbooruInstancedModel


class DanbooruTagImplication(DanbooruInstancedModel):
    reason: str
    creator_id: int
    antecedent_name: str
    consequent_name: str
    status: str
    approver_id: int | None
    forum_post_id: int | None
    forum_topic_id: int | None
