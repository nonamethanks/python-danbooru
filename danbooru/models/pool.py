"""Model definition for /pools."""


from __future__ import annotations

from typing import Literal

from danbooru.model import DanbooruInstancedModel


class DanbooruPool(DanbooruInstancedModel):
    name: str
    description: str
    is_active: bool
    is_deleted: bool
    category: Literal["series", "collection"]
    post_count: int
    post_ids: list[int]
