"""Model definition for /related_tag."""

from __future__ import annotations

from pydantic import BaseModel

from danbooru.model import DanbooruModel
from danbooru.models.tag import DanbooruTag
from danbooru.utils import classproperty


class RelatedTagData(BaseModel):
    tag: "DanbooruTag"
    cosine_similarity: float
    jaccard_similarity: float
    overlap_coefficient: float
    frequency: float


class DanbooruRelatedTag(DanbooruModel):
    query: str
    post_count: int

    tag: DanbooruTag

    related_tags: list[RelatedTagData]

    @classproperty
    def generic_endpoint(self) -> str:  # noqa: D102
        return "related_tag"
