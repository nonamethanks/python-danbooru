"""Model definition for /tags."""

import re
from functools import cached_property

from danbooru.model import DanbooruModel, _DanbooruModelWithId
from danbooru.models.tag_implication import DanbooruTagImplication
from danbooru.models.wiki_page import DanbooruWikiPage


class DanbooruTag(DanbooruModel, _DanbooruModelWithId):
    name: str
    post_count: int
    category: int
    is_deprecated: bool
    words: list[str]

    wiki_page: DanbooruWikiPage | None = None
    antecedent_implications: list[DanbooruTagImplication] | None = None

    @property
    def qualifiers(self) -> list[str]:
        """Return the qualifiers for the tag."""
        return re.findall(r"\((.*?)\)", self.name)

    def has_series_qualifier(self, qualifiers: list[str]) -> bool:
        """Whether this tag's last qualifier is a specific one."""
        return bool(self.qualifiers and self.qualifiers[-1] in qualifiers)

    @cached_property
    def related_copyrights(self) -> list["DanbooruTag"]:
        """Get a list of related copyrights for this tag."""
        min_related_value = 0.9

        from danbooru.models.related_tag import DanbooruRelatedTag

        related_tags = DanbooruRelatedTag.get(query=self.name, limit=10, category="Copyright").related_tags
        related_tags = list(filter(lambda x: x.frequency > min_related_value, related_tags))
        return [r.tag for r in related_tags]
