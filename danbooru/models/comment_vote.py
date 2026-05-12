"""Model definition for /comment_votes."""


from __future__ import annotations

from danbooru.model import DanbooruInstancedModel


class DanbooruCommentVote(DanbooruInstancedModel):
    comment_id: int
    user_id: int
