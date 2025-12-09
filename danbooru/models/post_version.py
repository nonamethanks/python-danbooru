"""Model definition for /post_versions."""


from pydantic import field_validator

from danbooru.model import DanbooruInstancedModel


class DanbooruPostVersion(DanbooruInstancedModel):
    created_at: None = None

    added_tags: list[str]
    removed_tags: list[str]
    obsolete_added_tags: list[str]
    obsolete_removed_tags: list[str]

    @field_validator("obsolete_added_tags", "obsolete_removed_tags", mode="before")
    def split_string(cls, v: str) -> str:
        """Turn the tag strings into tag arrays."""
        if isinstance(v, str):
            return v.split()
        return v
