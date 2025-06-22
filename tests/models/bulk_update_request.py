import pytest

from danbooru.model import WrongIncludeCallError
from danbooru.models.bulk_update_request import DanbooruBulkUpdateRequest


def test_burs() -> None:
    burs = DanbooruBulkUpdateRequest.get(limit=20)
    assert len(burs) == 20


def test_bur() -> None:
    bur, = DanbooruBulkUpdateRequest.get(id=10000)

    assert bur.id == 10000
    assert bur.user_id == 390810
    assert bur.forum_topic_id == 7713
    assert bur.script == "create alias dangogo99 -> dangogo"
    assert bur.status == "approved"
    assert bur.approver_id == 508240
    assert bur.forum_post_id == 211091
    assert bur.tags == ["dangogo", "dangogo99"]


def test_bur_no_forum_post() -> None:
    bur, = DanbooruBulkUpdateRequest.get(id=1000, include="forum_post")

    assert not bur.forum_post_id

    with pytest.raises(WrongIncludeCallError) as excinfo:
        _ = bur.forum_post

    assert "We don't have a value for 'forum_post' " in str(excinfo.value)
