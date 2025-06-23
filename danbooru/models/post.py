"""Model definition for /posts."""


from __future__ import annotations

from typing import Self

from danbooru.model import DanbooruInstancedModel


class DanbooruPost(DanbooruInstancedModel):
    tag_string: str

    @property
    def tags(self) -> list[str]:
        """Return an array of post tags."""
        return self.tag_string.split(" ")

    def update_tags(self, *tags: list[str]) -> Self:
        """Update a post's tags."""
        tag_string = " ".join(tags)
        data = {
            "tag_string": tag_string,
            "old_tag_string": "",
        }
        return self.update(**data)
