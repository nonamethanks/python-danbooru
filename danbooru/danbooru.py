"""Base session used throughout the module."""


import logging
import os
from datetime import timedelta

from backoff import constant, expo, on_exception
from dotenv import load_dotenv
from pyrate_limiter import Duration, Limiter, Rate
from requests import Response, Session
from requests.exceptions import JSONDecodeError, ReadTimeout
from requests_cache import CachedSession

from danbooru import logger
from danbooru.__version__ import package_version
from danbooru.exceptions import DanbooruRateLimitError, EmptyResponseError, RetriableDanbooruError, raise_http_exception
from danbooru.model import DanbooruInstancedModel, DanbooruModel, DanbooruModelType
from danbooru.report_model import DanbooruReportModel

load_dotenv()

logging.getLogger("backoff").addHandler(logging.StreamHandler())
logging.getLogger("backoff").setLevel(logging.ERROR)

request_rate = Rate(1, Duration.SECOND)
request_limiter = Limiter(request_rate, max_delay=10_000)


def backoff_handler(details: dict) -> None:
    """Handler for backoff function."""
    logger.error("Backing off {wait:0.1f} seconds after {tries} tries "
                 "calling function {target} with args {args} and kwargs "
                 "{kwargs}".format(**details))


class Danbooru:
    def __init__(self,
                 base_url: str = os.getenv("DANBOORU_BASE_URL", "https://testbooru.donmai.us"),
                 danbooru_username: str | None = os.getenv("DANBOORU_USERNAME"),
                 danbooru_api_key: str | None = os.getenv("DANBOORU_API_KEY"),
                 ) -> None:
        """Initialize a Danbooru session with base URL and optional authentication."""
        self.logger = logger

        self.base_url = base_url.strip("/")
        self.logger.trace(f"Setting base url: {base_url}")

        self._session = Session()
        self._cache_session = CachedSession(
            allowable_codes=range(200, 300),
            allowable_methods=["GET", "HEAD"],
            expire_after=timedelta(hours=1),
        )

        if danbooru_username and danbooru_api_key:
            self.logger.trace(f"Setting username: {danbooru_username}")
            self._session.auth = (danbooru_username, danbooru_api_key)
            self._cache_session.auth = (danbooru_username, danbooru_api_key)
        else:
            self.logger.trace("No username was configured. All requests will be anonymous.")

        headers = {
            "User-Agent": f"DanbooruTools/{package_version} <username='{danbooru_username or ""}'>",
            "Accept": "application/json",
        }
        self.logger.trace(f"Setting User Agent: {headers["User-Agent"]}.")
        self._session.headers = headers
        self._cache_session.headers = headers

    @on_exception(expo, (ReadTimeout, RetriableDanbooruError), max_tries=5, jitter=None, on_backoff=backoff_handler)
    @on_exception(constant, (DanbooruRateLimitError), max_tries=5, jitter=None, interval=60, on_backoff=backoff_handler)
    def danbooru_request(self,
                         method: str,
                         endpoint: str,
                         cache: bool = False,  # noqa: FBT001, FBT002
                         **kwargs,
                         ) -> list[DanbooruModelType] | list[DanbooruModel] | DanbooruModelType:
        """
        Send a request to the Danbooru api. The **kwargs are automatically parsed to be compatible with Rails parameters.

        For example, `danbooru_request("GET", "comments", id=1)` automatically converts the query params to ?search[id]=1.`
        """
        endpoint = endpoint.strip("/").removesuffix(".json")
        if method == "GET":
            kwargs["only"] = self._get_include(endpoint=endpoint, include=kwargs.pop("include", []), only=kwargs.pop("only", ""))
            kwargs = self._kwargs_to_rails_params(endpoint=endpoint, **kwargs)
            kwargs = {"params": kwargs}

        endpoint_url = f"{self.base_url}/{endpoint}".strip("/")

        response = self._do_request(method, endpoint_url, cache, **kwargs)

        if not response.ok:
            raise_http_exception(response)

        return self._parse_response(response, endpoint)

    def _do_request(self, method: str, endpoint_url: str, cache: bool, **kwargs) -> Response:  # noqa: FBT001
        if cache:
            response = self._cache_session.request(method, endpoint_url, only_if_cached=True, **kwargs)

        if not cache or (cache and response.status_code == 504):  # noqa: PLR2004
            request_limiter.try_acquire("request")
            if cache:
                response = self._cache_session.request(method, endpoint_url, **kwargs)
            else:
                response = self._session.request(method, endpoint_url, **kwargs)
            self.logger.trace(f"Performed {method} request for {response.request.url}")
        else:
            self.logger.trace(f"Retrieved cached {method} request for {response.request.url}")

        return response

    def _parse_response(self, response: Response, endpoint: str) -> list[DanbooruModelType] | list[DanbooruModel] | DanbooruModelType:
        try:
            data = response.json()
        except JSONDecodeError as e:
            if not response.content:
                raise EmptyResponseError(response,
                                         error_type="EmptyResponseError",
                                         error_message="The response was successful but nothing was returned.") from e
            raise NotImplementedError(response.content) from e

        model = DanbooruModel.model_for_endpoint(endpoint)
        if not issubclass(model, (DanbooruInstancedModel, DanbooruReportModel)) or response.request.method != "GET":
            if not isinstance(data, dict):
                msg = f"API returned unexpected type: {type(data)} => {data}"
                raise TypeError(msg, model)

            return model(**data, session=self, response=response)
        else:
            if not isinstance(data, list):
                msg = f"API returned unexpected type: {type(data)} => {data}"
                raise TypeError(msg, model)

            return [model(**obj, session=self, response=response) for obj in data]

    def _get_include(self, endpoint: str, include: list[str] | str | None = None, only: list[str] | str | None = None) -> str | None:
        if only:
            err = "Usage of only= is not supported. Use include= instead to include extra fields."
            raise ValueError(err)

        if not include:
            return None

        if isinstance(include, str):
            include = include.split(",")

        model = DanbooruModel.model_for_endpoint(endpoint)
        include = model.default_includes() + (include or [])

        include_str = ",".join(dict.fromkeys(include))
        return include_str

    @classmethod
    def _kwargs_to_rails_params(cls, endpoint: str, **kwargs) -> dict:
        """Turn kwargs into url parameters that Rails can understand."""
        params = {}

        if endpoint == "posts":
            params.setdefault("limit", 200)
        elif endpoint == "counts/posts":
            ...
        else:
            params.setdefault("limit", 1000)

        for named_parameter in ["only", "page", "limit"]:
            if n_p := kwargs.pop(named_parameter, None):
                params[named_parameter] = n_p

        for _key, _value in kwargs.items():
            if _key == "tags" and endpoint in ["posts", "counts/posts"]:
                params[_key] = _value
                continue

            parsed_key = f"search[{_key}]"
            for extra_key, parsed_value in cls._parse_to_include(_value):
                params[parsed_key + extra_key] = parsed_value
        return params

    @classmethod
    def _parse_to_include(cls, obj: str | dict) -> list[tuple[str, str]]:
        if isinstance(obj, dict):
            keys_and_values: list[tuple[str, str]] = []
            for [_key, _val] in obj.items():
                parsed_key = f"[{_key}]"
                for extra_key, parsed_value in cls._parse_to_include(_val):
                    keys_and_values.append((parsed_key + extra_key, parsed_value))
            return keys_and_values
        else:
            return [("", obj)]
