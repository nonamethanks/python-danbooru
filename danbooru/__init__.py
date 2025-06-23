"""The Danbooru package provides a model-based interface to the Danbooru API."""


from loguru import logger

from danbooru.danbooru import Danbooru  # noqa: F401
from danbooru.models import *  # noqa: F403
from danbooru.reports import *  # noqa: F403

logger = logger.opt(colors=True)
