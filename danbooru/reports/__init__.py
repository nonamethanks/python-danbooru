"""Defines the danbooru report models individually."""

import importlib
import pkgutil
from typing import TYPE_CHECKING

from danbooru import reports

if TYPE_CHECKING:
    from danbooru.model import DanbooruModelType

_report_models: list[type["DanbooruModelType"]] = []  # type: ignore[valid-type]

for _finder, name, _ispkg in pkgutil.iter_modules(reports.__path__, reports.__name__ + "."):
    submodule = importlib.import_module(name)
    for attr in dir(submodule):
        if attr.startswith("Danbooru"):
            report_model = getattr(submodule, attr)
            _report_models.append(report_model)
            globals()[attr] = report_model
