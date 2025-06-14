"""
Defines the base danbooru model that all other models inherit.

Uses pydantic for validation.
"""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Self, TypeVar, overload
from urllib.parse import urlencode, urlparse

import inflection

from danbooru.utils import BaseModel, classproperty

if TYPE_CHECKING:
    from requests import Response

    from danbooru.danbooru import Danbooru

DanbooruModelType = TypeVar("DanbooruModelType", bound="DanbooruModel")


class _DanbooruModelReturnsDict:
    ...


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
        if self.__class__.__name__ in ("DanbooruModel", "DanbooruReportModel"):
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
        return inflection.pluralize(endpoint)

    @classmethod
    def url_for(cls, **kwargs) -> str:
        """Return the canonical url for a model with params."""

        if not kwargs.pop("session", None):
            session = get_default_session()

        params = session._kwargs_to_rails_params(endpoint=cls.endpoint_name, **kwargs)  # noqa: SLF001
        param_string = urlencode(params)
        return f"{session.base_url}/{cls.endpoint_name}?{param_string}"

    @overload
    @classmethod
    def get(cls: type[_DanbooruModelReturnsDict], cache: bool = False, **kwargs) -> Self: ...  # noqa: FBT001, FBT002

    @overload
    @classmethod
    def get(cls, cache: bool = False, **kwargs) -> list[Self]: ...  # noqa: FBT001, FBT002

    @classmethod
    def get(cls, cache: bool = False, **kwargs) -> list[Self] | Self:  # noqa: FBT001, FBT002
        """Proxy for `Danbooru().danbooru_request("GET", endpoint, **kwargs)`. Accepts an optional `session` param."""
        if not kwargs.pop("session", None):
            session = get_default_session()

        if not cls.endpoint_name.startswith(("reports/", "counts/")):
            kwargs.setdefault("limit", 1)

        response = session.danbooru_request("GET", cls.endpoint_name, cache=cache ** kwargs)
        return response  # type: ignore[return-value]

    @classmethod
    def get_all(cls, **kwargs) -> list[Self]:
        """Get all elements for a specific search. Accepts an optional `session` param."""
        if not kwargs.pop("session", None):
            session = get_default_session()

        kwargs.pop("page", None)
        kwargs.pop("limit", None)
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
        for model in cls.all_models:
            if model.model_name == name:  # type: ignore[attr-defined]
                return model
        return cls

    @classmethod
    def model_for_endpoint(cls, endpoint: str) -> type[DanbooruModelType | DanbooruModel]:
        """Get the right model from an endpoint."""
        for model in cls.all_models:
            if model == DanbooruModel:
                continue

            if model.endpoint_name == endpoint:  # type: ignore[attr-defined]
                return model
        return cls

    @classproperty
    def all_models(self) -> list[type[DanbooruModelType]]:
        """Return all subclasses."""
        from danbooru.models import _models
        from danbooru.reports import _report_models
        return _models + _report_models


g = {}


def get_default_session() -> Danbooru:
    """Instantiate a default session if none is passed to the model."""
    if not g.get("session"):
        from danbooru.danbooru import Danbooru
        g["session"] = Danbooru()
    return g["session"]
