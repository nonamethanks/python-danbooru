"""Model definition for /counts/posts."""


from danbooru.model import DanbooruModel, _DanbooruModelReturnsDict
from danbooru.utils import BaseModel, classproperty


class _Counts(BaseModel):
    posts: int


class DanbooruPostCounts(DanbooruModel, _DanbooruModelReturnsDict):
    counts: _Counts

    @classproperty
    def endpoint_name(self) -> str:  # noqa: D102
        return "counts/posts"

    @property
    def count(self) -> int:
        """Shortcut for `.counts.posts`."""
        return self.counts.posts
