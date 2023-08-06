# pylint: disable=too-few-public-methods
"""
Module for parsing English language txt file.
"""
from loguru import logger


STRUCTURE_NAMES = {
    "cover": "Cover",
}


class EnParser:
    """
    Module for parsing txt format in en.
    """

    def __init__(self, content: str, config: dict) -> None:
        self.raw_content = content
        self.config = config

    def parse(self) -> tuple:
        """
        Parse the content into volumes (optional) and chapters.
        """
        logger.info("Volumes parsed: 0")
        logger.error("Chapters parsed: 0")
        return (self.raw_content, self.raw_content)
