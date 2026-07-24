"""Model definition for /posts."""


from __future__ import annotations

import time
from typing import Self

from danbooru import logger
from danbooru.exceptions import DanbooruHTTPError
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

    @classmethod
    def expunge(cls, post_id: int) -> None:
        from danbooru.danbooru import Danbooru
        session = Danbooru()
        assert post_id > 11_000_000
        logger.info(f"Permanently expunging post #{post_id}")
        try:
            session.danbooru_request(
                "POST",
                f"moderator/post/posts/{post_id}/expunge",
                params={"post_id": post_id},
            )
        except DanbooruHTTPError as e:
            if e.response.status_code == 406:
                return
            if e.response.status_code == 500:
                time.sleep(5)
            else:
                raise
