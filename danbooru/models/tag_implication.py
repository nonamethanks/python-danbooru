"""Model definition for /tag_implications."""

from danbooru.model import DanbooruModel


class DanbooruTagImplication(DanbooruModel):
    reason: str
    creator_id: int
    antecedent_name: str
    consequent_name: str
    status: str
    forum_topic_id: int
    approver_id: int
    forum_post_id: int | None
