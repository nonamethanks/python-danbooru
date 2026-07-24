"""Model definition for /post_approvals."""


from __future__ import annotations

from danbooru.model import DanbooruInstancedModel


class DanbooruPostApproval(DanbooruInstancedModel):
    post_id: int
    user_id: int
