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

    @field_validator("added_tags", "removed_tags", "obsolete_added_tags", "obsolete_removed_tags", mode="before")
    @classmethod
    def filter_null_tags(cls, v):  # noqa: ANN001, ANN206
        """https://github.com/danbooru/danbooru/issues/6365."""
        if isinstance(v, list):
            return [item for item in v if item is not None]
        return v

    @property
    def url(self) -> str:
        return f"{self._session.base_url}/post_versions?search[post_id]={self.post_id}#post-version-{self.id}"

    @property
    def is_reverted(self) -> bool:
        actual_added = [t for t in self.added_tags if t not in self.obsolete_added_tags]
        actual_removed = [t for t in self.removed_tags if t not in self.obsolete_removed_tags]
        return not actual_added and not actual_removed
