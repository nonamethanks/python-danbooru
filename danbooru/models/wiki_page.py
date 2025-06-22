"""Model definition for /wiki_pages."""
import re

from danbooru.model import DanbooruModel, _DanbooruModelWithId


class DanbooruWikiPage(DanbooruModel, _DanbooruModelWithId):
    title: str
    body: str
    is_locked: bool
    other_names: list[str]
    is_deleted: bool

    @property
    def linked_tags(self) -> list[str]:
        """Return a list of linked tags in a wiki's body."""
        pattern = re.compile(r"\[\[([^|\[\]]+)(?:\|(.*))?\]\]")

        tags = [t[0].strip() for t in pattern.findall(self.body)]
        return [t.replace(" ", "_").lower() for t in tags]
