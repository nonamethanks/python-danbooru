"""Model definition for /users."""

import datetime

from danbooru.model import DanbooruInstancedModel
from danbooru.user_level import UserLevel


class DanbooruUser(DanbooruInstancedModel):
    level: UserLevel
    updated_at: datetime.datetime | None = None
