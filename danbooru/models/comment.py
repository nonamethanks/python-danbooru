"""Model definition for /comments."""


from danbooru.model import DanbooruInstancedModel


class DanbooruComment(DanbooruInstancedModel):
    post_id: int
    creator_id: int
    body: str
    score: int
    updater_id: int
    do_not_bump_post: bool
    is_deleted: bool
    is_sticky: bool
