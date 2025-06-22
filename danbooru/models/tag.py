"""Model definition for /tags."""

from danbooru.model import DanbooruModel
from danbooru.models.tag_implication import DanbooruTagImplication
from danbooru.models.wiki_page import DanbooruWikiPage


class DanbooruTag(DanbooruModel):
    name: str
    post_count: int
    category: int
    is_deprecated: bool
    words: list[str]

    wiki_page: DanbooruWikiPage | None = None
    antecedent_implications: list[DanbooruTagImplication] | None = None
