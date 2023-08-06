"""
Module for generating txt file.
"""
import os
from datetime import datetime as dt
from pathlib import Path

from loguru import logger

from ..models import Book


class TxtWriter:
    """
    Module for writing ebook in txt format.
    """

    def __init__(self, book: Book, opts: dict) -> None:
        self.book = book
        self.filename = opts["input_file"]
        self.no_backup = opts["no_backup"]

    def write(self) -> None:
        """
        Optionally backup and overwrite the txt file.
        """
        if not self.no_backup:
            self._backup_file()

        self._overwrite_file()

    def _backup_file(self) -> None:
        txt_filename = Path(self.filename)

        ymd_hms = dt.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = Path(
            txt_filename.resolve().parent.joinpath(
                txt_filename.stem + "_" + ymd_hms + ".bak.txt"
            )
        )
        os.rename(txt_filename, backup_filename)
        logger.info("Backup txt file: {}", backup_filename)

    def _overwrite_file(self) -> None:
        txt_filename = Path(self.filename)

        with open(txt_filename, "w", encoding="utf8") as file:
            file.write(self.book.massaged_content)
            logger.info("Overwrite txt file: {}", txt_filename.resolve())
