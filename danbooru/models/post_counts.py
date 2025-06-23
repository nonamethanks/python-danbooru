"""Model definition for /counts/posts."""


from danbooru.model import DanbooruModel
from danbooru.utils import BaseModel, classproperty


class _Counts(BaseModel):
    posts: int


class DanbooruPostCounts(DanbooruModel):
    counts: _Counts

    @classproperty
    def generic_endpoint(self) -> str:  # noqa: D102
        return "counts/posts"

    @property
    def count(self) -> int:
        """Shortcut for `.counts.posts`."""
        return self.counts.posts
