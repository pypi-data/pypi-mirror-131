# pylint: disable=no-value-for-parameter
"""
Main module for txt2ebook console app.
"""

import sys
from pathlib import Path
from typing import Dict

from bs4 import UnicodeDammit
from configuror import Config
from loguru import logger
import click

from txt2ebook import __version__
from txt2ebook.parsers import create_parser
from txt2ebook.formatters import create_formatter


@click.command(no_args_is_help=True)
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(), required=False)
@click.option(
    "--format",
    "-f",
    default="epub",
    show_default=True,
    help="Set the export format ebook.",
)
@click.option(
    "--title",
    "-t",
    default=None,
    show_default=True,
    help="Set the title of the ebook.",
)
@click.option(
    "--language",
    "-l",
    default=None,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    multiple=True,
    help="Set the author of the ebook.",
)
@click.option(
    "--cover",
    "-c",
    type=click.Path(exists=True),
    default=None,
    help="Set the cover of the ebook.",
)
@click.option(
    "--width",
    "-w",
    type=click.INT,
    show_default=True,
    help="Set the width for line wrapping.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value="DEBUG",
    show_default=True,
    help="Enable debugging log.",
)
@click.option(
    "--test-parsing",
    "-tp",
    is_flag=True,
    show_default=True,
    help="Test parsing only for volume/chapter header.",
)
@click.option(
    "--no-backup",
    "-nb",
    is_flag=True,
    flag_value=True,
    show_default=True,
    help="Do not backup source txt file.",
)
@click.option(
    "--no-wrapping",
    "-nw",
    is_flag=True,
    show_default=True,
    help="Remove word wrapping.",
)
@click.option(
    "--epub-template",
    "-et",
    default="clean",
    show_default=True,
    help="CSS template for EPUB.",
)
@click.option(
    "--delete-regex",
    "-dr",
    multiple=True,
    help="Regex to delete word or phrase.",
)
@click.option(
    "--replace-regex",
    "-rr",
    nargs=2,
    multiple=True,
    help="Regex to replace word or phrase.",
)
@click.option(
    "--delete-line-regex",
    "-dlr",
    multiple=True,
    help="Regex to delete whole line.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
def main(**kwargs: Dict) -> None:
    """
    Console tool to convert txt file to different ebook format.
    """
    config = Config(**kwargs)

    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{level: >5}</green>: {message}",
        level=config["test_parsing"] and "DEBUG" or config["debug"] or "INFO",
        colorize=True,
    )

    try:
        filename = Path(config["input_file"])
        logger.info("Parsing txt file: {}", filename.resolve())

        with open(filename, "rb") as file:
            unicode = UnicodeDammit(file.read())
            logger.info("Detect encoding : {}", unicode.original_encoding)
            content = unicode.unicode_markup

            if not content:
                raise RuntimeError(f"Empty file content in {filename}")

            parser = create_parser(content, config)
            book = parser.parse()

            if config["test_parsing"] or config["debug"]:
                logger.debug(repr(book))

                for volume in book.volumes:
                    logger.debug(repr(volume))
                    for chapter in volume.chapters:
                        logger.debug(repr(chapter))

                for chapter in book.chapters:
                    logger.debug(repr(chapter))

            if not config["test_parsing"]:
                if book.parsed_content:
                    writer = create_formatter(book, config)
                    writer.write()

                # We write to txt for debugging purpose if output format is not
                # txt.
                if config["format"] != "txt":
                    config["format"] = "txt"
                    txt_writer = create_formatter(book, config)
                    txt_writer.write()

    except RuntimeError as error:
        logger.error(str(error))


if __name__ == "__main__":
    main()
