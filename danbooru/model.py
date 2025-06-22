"""
Defines the base danbooru model that all other models inherit.

Uses pydantic for validation.
"""
from __future__ import annotations

import datetime
from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Self, TypeVar, overload
from urllib.parse import parse_qs, urlencode, urlparse

import inflection
from loguru import logger

from danbooru.utils import BaseModel, classproperty

if TYPE_CHECKING:
    from collections.abc import Generator

    from pydantic.fields import FieldInfo
    from requests import PreparedRequest, Response

    from danbooru.danbooru import Danbooru

DanbooruModelType = TypeVar("DanbooruModelType", bound="DanbooruModel")


class _DanbooruModelReturnsDict:
    ...


class _DanbooruModelWithId(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class WrongIncludeCallError(Exception):
    def __init__(self, value: str):
        """Raise an exception when an optional parameter was not passed to the query, but it's still accessed in the model."""
        super().__init__(f"We don't have a value for '{value}' because "
                         "it was not passed to the query through the only= parameter, or it's missing from the api.")


_parent_data = ContextVar("_parent_data")


class DanbooruModel(BaseModel):
    def __init__(self, *, response: Response | None = None, session: Danbooru | None = None, **data):
        """Declare a generic Danbooru model as fallback in case the specific ones aren't defined."""

        with self._bind({"session": session or _parent_data.get().get("session"),
                         "response": response or _parent_data.get().get("response")}):
            session = session or _parent_data.get().get("session")
            response = response or _parent_data.get().get("response")
            super().__init__(**data, response=response, session=session)

            self._request = response.request
            self._response = response
            self._session = session

    @classmethod
    @contextmanager
    def _bind(cls, parent_data: dict):  # noqa: ANN206
        token = _parent_data.set(parent_data)
        try:
            yield cls
        finally:
            _parent_data.reset(token)

    @classmethod
    def default_includes(cls) -> list[str]:
        """Default includes for the model."""
        return [name for name, field in cls.model_fields.items() if field.is_required()]

    def __getattribute__(self, name: str):
        """Override to skip validation for the response."""
        field: FieldInfo | None = super().__getattribute__("model_fields").get(name)
        value = super().__getattribute__(name)

        if not field:
            return value

        if not field.is_required() and value is None:
            request: PreparedRequest = super().__getattribute__("_request")
            params = parse_qs(urlparse(request.url).query).get("only", [])
            if params:
                params = params[0].split(",")
            params = params or super().__getattribute__("default_includes")

            if name not in params:
                raise WrongIncludeCallError(name)

        return value

    @property
    def url(self) -> str:
        """The url to the model instance."""
        if self.__class__.__name__ in ("DanbooruModel", "DanbooruReportModel"):
            return self._response.url

        url = f"{self._session.base_url}/{self.endpoint_name}"

        if isinstance(self, _DanbooruModelWithId):
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

        response = session.danbooru_request("GET", cls.endpoint_name, cache=cache, **kwargs)
        return response  # type: ignore[return-value]

    @classmethod
    def get_all(cls, **kwargs) -> list[Self]:
        """Get all elements for a specific search. Accepts an optional `session` param."""
        return [m for p in cls.all_pages(**kwargs) for m in p]

    @classmethod
    def all_pages(cls, **kwargs) -> Generator[list[Self], None, None]:
        """Loop through the pages of a specific search. Accepts an optional `session` param."""
        if not kwargs.pop("session", None):
            session = get_default_session()

        kwargs.pop("page", None)
        kwargs.pop("limit", None)
        page = 1

        limit = 200 if cls.endpoint_name == "posts" else 1000

        while True:
            response = session.danbooru_request("GET", cls.endpoint_name, page=page, limit=limit, **kwargs)
            if response:
                yield response
            if len(response) < limit:
                logger.trace(f"Got {len(response)} (<{limit}) {cls.endpoint_name} on page {page}, stopping.")
                return
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

    def __hash__(self):
        return hash(self.url)


g = {}


def get_default_session() -> Danbooru:
    """Instantiate a default session if none is passed to the model."""
    if not g.get("session"):
        from danbooru.danbooru import Danbooru
        g["session"] = Danbooru()
    return g["session"]
