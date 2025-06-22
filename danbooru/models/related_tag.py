"""Model definition for /related_tag."""

from __future__ import annotations

from pydantic import BaseModel

from danbooru.model import DanbooruModel, _DanbooruModelReturnsDict
from danbooru.models.tag import DanbooruTag
from danbooru.utils import classproperty


class RelatedTagData(BaseModel):
    tag: "DanbooruTag"
    cosine_similarity: float
    jaccard_similarity: float
    overlap_coefficient: float
    frequency: float


class DanbooruRelatedTag(DanbooruModel, _DanbooruModelReturnsDict):
    query: str
    post_count: int

    tag: "DanbooruTag"

    related_tags: list[RelatedTagData]

    @classproperty
    def endpoint_name(self) -> str:  # noqa: D102
        return "related_tag"
