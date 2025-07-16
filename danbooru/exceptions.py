"""Defines common exceptions."""

import requests


def raise_http_exception(response: requests.Response) -> None:
    """Raise the appropriate exception for a bad request."""
    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError:
        if "Danbooru is down for maintenance" in response.text:
            error_type = "Downbooru"
            error_message = "The site is down for maintenance."
            raise DownbooruError(response, error_type=error_type, error_message=error_message) from None
        if ("<center><h1>502 Bad Gateway</h1></center>" in response.text
                and "<center>cloudflare</center>" in response.text):
            error_type = "CloudflareError"
            error_message = "Cloudflare has blocked this request."
            raise CloudflareError(response, error_type=error_type, error_message=error_message) from None
        raise
    else:
        try:
            error_type = json_response["error"]
        except KeyError as e:
            raise NotImplementedError(response.json()) from e

        error_message = json_response["message"]
        backtrace = json_response["backtrace"]

        if error_type == "ActiveRecord::QueryCanceled":
            raise DanbooruTimeoutError(response, error_type=error_type, error_message=error_message, backtrace=backtrace)

        raise DanbooruHTTPError(response, error_type=error_type, error_message=error_message, backtrace=backtrace)


class DanbooruHTTPError(Exception):
    """A danbooru HTTP error."""

    def __init__(self,
                 response: requests.Response,
                 error_type: str,
                 error_message: str,
                 backtrace: list[str] | None = None,
                 *args, **kwargs) -> None:
        """Represent a generic Danbooru error."""
        self.error_type = error_type
        self.error_message = error_message
        self.backtrace = backtrace or []
        self.response = response

        super().__init__(self.message, * args, **kwargs)

    @property
    def message(self) -> str:
        """The exception message."""
        msg = f"{self.error_type} - {self.error_message}"
        msg += f"\n    Status code: {self.response.status_code}"
        msg += f"\n    On page: {self.response.request.url}"
        if self.backtrace:
            msg += "\n    Backtrace:"
            for row in self.backtrace:
                msg += f"\n     {row}"
        return msg


class EmptyResponseError(DanbooruHTTPError):
    """The response was empty, but the request was successful."""


class RetriableDanbooruError(DanbooruHTTPError):
    """An error that can be retried."""


class DownbooruError(RetriableDanbooruError):
    """Site's down for maintenance."""


class DanbooruTimeoutError(RetriableDanbooruError):
    """Your query took too long."""


class CloudflareError(RetriableDanbooruError):
    """Generic Cloudflare error."""
