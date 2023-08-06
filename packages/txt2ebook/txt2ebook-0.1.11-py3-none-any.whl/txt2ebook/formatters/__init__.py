"""
Subpackages for writing different ebook format.
"""
from typing import Any

from ..helpers import to_classname, load_class
from .epub import EpubWriter
from .txt import TxtWriter

from ..models import Book


def create_formatter(book: Book, config: dict) -> Any:
    """
    Factory method to create ebook formatter by format.
    """
    class_name = to_classname(config["format"], "Writer")
    klass = load_class("txt2ebook.formatters", class_name)
    formatter = klass(book, config)
    return formatter
