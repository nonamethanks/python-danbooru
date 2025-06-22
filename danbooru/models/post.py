"""Model definition for /posts."""

from danbooru.model import DanbooruModel, _DanbooruModelWithId


class DanbooruPost(DanbooruModel, _DanbooruModelWithId):
    tag_string: str

    @property
    def tags(self) -> list[str]:
        """Return an array of post tags."""
        return self.tag_string.split(" ")
