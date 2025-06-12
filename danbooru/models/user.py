"""Model definition for /users."""

from danbooru.model import DanbooruModel
from danbooru.user_level import UserLevel


class DanbooruUser(DanbooruModel):
    level: UserLevel
