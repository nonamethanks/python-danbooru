"""Model definition for /tags."""

from danbooru.model import DanbooruModel


class DanbooruTag(DanbooruModel):
    name: str
    post_count: int
    category: int
    is_deprecated: bool
    words: list[str]
