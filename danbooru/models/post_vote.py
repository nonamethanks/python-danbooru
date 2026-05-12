"""Model definition for /post_votes."""


from __future__ import annotations

from danbooru.model import DanbooruInstancedModel


class DanbooruPostVote(DanbooruInstancedModel):
    post_id: int
    user_id: int
