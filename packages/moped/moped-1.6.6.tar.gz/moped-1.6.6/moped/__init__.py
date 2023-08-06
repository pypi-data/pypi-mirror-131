import logging
import os

from . import databases, topological
from .core.compound import Compound
from .core.model import Model
from .core.reaction import Reaction

__all__ = ["databases", "topological", "Compound", "Model", "Reaction"]

logger = logging.getLogger("moped")
logger.setLevel(logging.WARNING)
formatter = logging.Formatter(
    fmt="{asctime} - {levelname} - {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

os.environ["LC_ALL"] = "C"  # meneco bugfix
