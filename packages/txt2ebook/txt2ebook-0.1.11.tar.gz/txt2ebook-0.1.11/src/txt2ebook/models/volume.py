"""
Module for a volume of a book model.
"""
from dataclasses import dataclass, field

from .chapter import Chapter


@dataclass
class Volume:
    """
    A volume class model.
    """

    title: str = field(default="")
    chapters: list[Chapter] = field(default_factory=list, repr=False)
    raw_content: str = field(default="", repr=False)
