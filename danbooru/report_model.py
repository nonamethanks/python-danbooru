"""Model definition for reports."""

from __future__ import annotations

import datetime

import inflection

from danbooru.model import DanbooruModel
from danbooru.user_level import UserLevel
from danbooru.utils import classproperty


class DanbooruReportModel(DanbooruModel):
    date: datetime.datetime = None
    level: UserLevel | None = None

    def __repr__(self) -> str:
        props = " ".join(f"{k}={v}" for k, v in self.model_dump(exclude_none=True).items())
        return f"{type(self).__name__}[{props}]"

    @classproperty
    def endpoint_name(self) -> str:
        """Autogenerates the endpoint name."""
        endpoint = self.model_name.removesuffix("_report")
        endpoint = f"reports/{endpoint}"
        return inflection.pluralize(endpoint)
