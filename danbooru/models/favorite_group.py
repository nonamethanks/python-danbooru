"""Model definition for /favorite_groups."""


from __future__ import annotations

from danbooru.model import DanbooruInstancedModel


class DanbooruFavoriteGroup(DanbooruInstancedModel):
    name: str
    creator_id: int

    post_ids: list[int]
    is_public: bool
