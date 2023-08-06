"""
Module for a chapter model of a book.
"""
from dataclasses import dataclass, field


@dataclass
class Chapter:
    """
    A chapter class model.
    """

    title: str = field(default="")
    raw_content: str = field(default="", repr=False)
    paragraphs: list[str] = field(default_factory=list, repr=False)
