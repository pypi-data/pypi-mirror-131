"""
Subpackage for helper function
"""

import sys
from importlib import import_module
from typing import Any

from loguru import logger


def to_classname(words: str, suffix: str) -> str:
    """
    Generate class name from words.
    """
    return words.replace("-", " ").title().replace(" ", "") + suffix


def load_class(package_name: str, class_name: str) -> Any:
    """
    Load class dynamically.
    """
    try:
        package = import_module(package_name)
        klass = getattr(package, class_name)
        logger.debug("Load module: {}.{}", package_name, class_name)
        return klass
    except AttributeError:
        logger.error("Fail to load module: {}.{}", package_name, class_name)
        sys.exit()
