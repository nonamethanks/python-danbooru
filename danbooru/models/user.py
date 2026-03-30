"""Model definition for /users."""

import datetime

from danbooru.model import DanbooruInstancedModel, get_default_session
from danbooru.user_level import UserLevel


class DanbooruUser(DanbooruInstancedModel):
    name: str
    level: UserLevel
    post_upload_count: int
    post_update_count: int
    note_update_count: int
    is_deleted: bool
    is_banned: bool

    updated_at: datetime.datetime | None = None  # not present

    # only present on /users/:id, not on index
    wiki_page_version_count: int | None = None
    artist_version_count: int | None = None
    artist_commentary_version_count: int | None = None
    forum_post_count: int | None = None
    pool_version_count: int | None = None
    comment_count: int | None = None
    appeal_count: int | None = None

    positive_feedback_count: int | None = None
    neutral_feedback_count: int | None = None
    negative_feedback_count: int | None = None

    @classmethod
    def get_from_name(cls, name: str, cache: bool = False) -> "DanbooruUser":
        """Get the extra user data that is not available from the /users index."""
        session = get_default_session()
        response = session._do_request("GET", "users", cache=cache, params={"name": name})  # noqa: SLF001
        return DanbooruUser(**response.json(), response=response, session=session)
