"""Defines the danbooru models individually."""

import importlib
import pkgutil
from typing import TYPE_CHECKING

from danbooru import models

if TYPE_CHECKING:
    from danbooru.model import DanbooruModelType

_models: list[type["DanbooruModelType"]] = []  # type: ignore[valid-type]

for _finder, name, _ispkg in pkgutil.iter_modules(models.__path__, models.__name__ + "."):
    submodule = importlib.import_module(name)
    for attr in dir(submodule):
        if attr.startswith("Danbooru"):
            model = getattr(submodule, attr)
            _models.append(model)
            globals()[attr] = model
