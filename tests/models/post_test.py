from danbooru.models.post import DanbooruPost


def test_post() -> None:
    p, = DanbooruPost.get(tags=["id:1"])

    assert p.id == 1
    assert "1girl" in p.tags


def test_no_post() -> None:
    assert DanbooruPost.get(tags=["id:6"]) == []
