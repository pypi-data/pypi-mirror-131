"""
Subpackage for all Parsers.
"""
from typing import Any

from langdetect import detect
from loguru import logger

from ..helpers import to_classname, load_class
from .zhcn import ZhCnParser
from .zhtw import ZhTwParser
from .en import EnParser


def create_parser(content: str, config: dict) -> Any:
    """
    Factory function to create parser by language.
    """
    config["language"] = detect_language(content, config["language"])
    class_name = to_classname(config["language"], "Parser")
    klass = load_class("txt2ebook.parsers", class_name)
    parser = klass(content, config)
    return parser


def detect_language(content: str, default: str) -> str:
    """
    Detect the language (ISO 639-1) of the content of the txt file.
    """
    language = default or detect(content)
    logger.info("Detect language: {}", language)
    return language
