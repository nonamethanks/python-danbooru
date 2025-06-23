"""Model definition for /users."""

from danbooru.model import DanbooruInstancedModel
from danbooru.user_level import UserLevel


class DanbooruUser(DanbooruInstancedModel):
    level: UserLevel
