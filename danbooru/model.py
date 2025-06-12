"""
Defines the base danbooru model that all other models inherit.

Uses pydantic for validation.
"""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Self, TypeVar
from urllib.parse import urlparse

import inflection

from danbooru.utils import BaseModel, classproperty

if TYPE_CHECKING:
    from requests import Response

    from danbooru.danbooru import Danbooru

DanbooruModelType = TypeVar("DanbooruModelType", bound="DanbooruModel")


class DanbooruModel(BaseModel):
    id: int = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    def __init__(self, *, response: Response, session: Danbooru, **data):
        """Declare a generic Danbooru model as fallback in case the specific ones aren't defined."""
        super().__init__(**data)
        self._request = response.request
        self._response = response
        self._session = session

    @property
    def url(self) -> str:
        """The url to the model instance."""
        if self.__class__ == DanbooruModel:
            return self._response.url

        url = f"{self._session.base_url}/{self.endpoint_name}"
        if self.id:
            return f"{url}/{self.id}"

        if (query := urlparse(self._request.url).query):
            url = f"{url}?{query}"

        return url

    def __repr__(self) -> str:
        return f"{type(self).__name__}<{self.url}>"

    @classproperty
    def model_name(self) -> str:
        """Autogenerates the model name."""
        class_name = self.__name__  # type: ignore[attr-defined]
        snake_name = inflection.underscore(class_name)

        return snake_name.removeprefix("danbooru_")

    @classproperty
    def endpoint_name(self) -> str:
        """Autogenerates the endpoint name."""
        endpoint = self.model_name
        if endpoint.endswith("_report"):
            endpoint = endpoint.removesuffix("_report")
            endpoint = f"reports/{endpoint}"

        return inflection.pluralize(endpoint)

    @classmethod
    def get(cls, session: Danbooru | None = None, **kwargs) -> list[Self]:
        """Proxy for `Danbooru().danbooru_request("GET", endpoint, **kwargs)`."""
        if not session:
            session = get_default_session()

        if not cls.endpoint_name.startswith(("reports/", "counts/")):
            kwargs.setdefault("limit", 1)

        response = session.danbooru_request("GET", cls.endpoint_name, **kwargs)
        return response  # type: ignore[return-value]

    @classmethod
    def get_all(cls, session: Danbooru | None = None, **kwargs) -> list[Self]:
        """Get all elements for a specific search."""
        if not session:
            session = get_default_session()

        kwargs.pop("page")
        kwargs.pop("limit")
        collected = []
        page = 1

        limit = 200 if cls.model_name == "posts" else 1000

        while True:
            response = session.danbooru_request("GET", cls.endpoint_name, page=page, limit=limit, **kwargs)
            collected += response
            if len(response) < limit:
                return collected
            page += 1

    @classmethod
    def model_for_name(cls, name: str) -> type[DanbooruModelType | DanbooruModel]:
        """Get the right model from an endpoint."""
        from danbooru.models import _models
        for model in _models:
            if model.model_name == name:  # type: ignore[attr-defined]
                return model
        return cls

    @classmethod
    def model_for_endpoint(cls, endpoint: str) -> type[DanbooruModelType | DanbooruModel]:
        """Get the right model from an endpoint."""
        from danbooru.models import _models
        for model in _models:
            if model == DanbooruModel:
                continue

            if model.endpoint_name == endpoint:  # type: ignore[attr-defined]
                return model
        return cls


g = {}


def get_default_session() -> Danbooru:
    """Instantiate a default session if none is passed to the model."""
    if not g.get("session"):
        from danbooru.danbooru import Danbooru
        g["session"] = Danbooru()
    return g["session"]
