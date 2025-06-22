"""Model definition for /users."""

from danbooru.model import DanbooruModel, _DanbooruModelWithId
from danbooru.user_level import UserLevel


class DanbooruUser(DanbooruModel, _DanbooruModelWithId):
    level: UserLevel
