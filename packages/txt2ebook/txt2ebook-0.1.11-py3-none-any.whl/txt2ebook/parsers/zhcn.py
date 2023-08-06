"""
Module for parsing Simplified Chinese language txt file.
"""
import re

import cjkwrap
from loguru import logger

from ..models import Book, Volume, Chapter


IDEOGRAPHIC_SPACE = "\u3000"
SPACE = "\u0020"
NUMS_WORDS = "零一二三四五六七八九十百千两"
FULLWIDTH_NUMS = "０１２３４５６７８９"

RE_TITLE = r"书名：(.*)|【(.*)】|《(.*)》"
RE_AUTHOR = r"作者：(.*)"
RE_WHITESPACES = f"[{SPACE}\t{IDEOGRAPHIC_SPACE}]"
RE_NUMS = f"[.0-9{FULLWIDTH_NUMS}{NUMS_WORDS}]"
RE_VOLUME = f"^{RE_WHITESPACES}*第{RE_NUMS}*[集卷册][^。~\n]*$"
RE_CHAPTER = "|".join(
    [
        f"^{RE_WHITESPACES}*第{RE_NUMS}*[章篇回折].*$",
        f"^{RE_WHITESPACES}*[楔引]子[^，].*$",
        f"^{RE_WHITESPACES}*序[章幕曲]?$",
        f"^{RE_WHITESPACES}*前言.*$",
        f"^{RE_WHITESPACES}*[内容]*简介.*$",
        f"^{RE_WHITESPACES}*[号番]外篇.*$",
        f"^{RE_WHITESPACES}*尾声$",
    ]
)

STRUCTURE_NAMES = {
    "cover": "封面",
}


class ZhCnParser:
    """
    Module for parsing txt format in zh-cn.
    """

    def __init__(self, content: str, config: dict) -> None:
        self.raw_content = content
        self.book_title = config["title"]
        self.authors = config["author"]
        self.cover = config["cover"]
        self.delete_regex = config["delete_regex"]
        self.replace_regex = config["replace_regex"]
        self.delete_line_regex = config["delete_line_regex"]
        self.no_wrapping = config["no_wrapping"]
        self.width = config["width"]

    def parse(self) -> Book:
        """
        Parse the content into volumes (optional) and chapters.
        """
        massaged_content = self.massage()
        (parsed_content, volumes, chapters) = self.parse_content(
            massaged_content
        )

        return Book(
            title=self.detect_book_title(),
            language="zh-cn",
            authors=self.detect_authors(),
            cover=self.cover,
            raw_content=self.raw_content,
            massaged_content=massaged_content,
            parsed_content=parsed_content,
            volumes=volumes,
            chapters=chapters,
            structure_names=STRUCTURE_NAMES,
        )

    def detect_book_title(self) -> str:
        """
        Extract book title from the content of the txt file.
        """
        if self.book_title:
            return self.book_title

        match = re.search(RE_TITLE, self.raw_content)
        if match:
            book_title = next(
                (title.strip() for title in match.groups() if title)
            )
            logger.info("Found book title: {}", book_title)
            return book_title

        logger.info("No book title found from file!")
        return ""

    def detect_authors(self) -> list:
        """
        Extract author from the content of the txt file.
        """
        if self.authors:
            return self.authors

        match = re.search(RE_AUTHOR, self.raw_content)
        if match:
            author = match.group(1).strip()
            logger.info("Found author: {}", author)
            return [author]

        logger.info("No author found from file!")
        return []

    def massage(self) -> str:
        """
        Massage the txt content.
        """
        content = self.raw_content

        content = ZhCnParser.to_unix_newline(content)

        if self.delete_regex:
            content = self.do_delete_regex(content)

        if self.replace_regex:
            content = self.do_replace_regex(content)

        if self.delete_line_regex:
            content = self.do_delete_regex(content)

        if self.no_wrapping:
            content = self.do_no_wrapping(content)

        if self.width:
            content = self.do_wrapping(content)

        return content

    @staticmethod
    def to_unix_newline(content: str) -> str:
        """
        Convert all other line ends to Unix line end.
        """
        return content.replace("\r\n", "\n").replace("\r", "\n")

    def do_delete_regex(self, content: str) -> str:
        """
        Remove words/phrases based on regex.
        """
        for delete_regex in self.delete_regex:
            content = re.sub(
                re.compile(rf"{delete_regex}", re.MULTILINE), "", content
            )
        return content

    def do_replace_regex(self, content: str) -> str:
        """
        Replace words/phrases based on regex.
        """
        for search, replace in self.replace_regex:
            content = re.sub(
                re.compile(rf"{search}", re.MULTILINE), rf"{replace}", content
            )
        return content

    def do_delete_line_regex(self, content: str) -> str:
        """
        Delete whole line based on regex.
        """
        for delete_line_regex in self.delete_line_regex:
            content = re.sub(
                re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
                "",
                content,
            )
        return content

    @staticmethod
    def do_no_wrapping(content: str) -> str:
        """
        Remove wrapping. Paragraph should be in one line.
        """
        # Convert to single spacing before we removed wrapping.
        lines = content.split("\n")
        content = "\n\n".join([line.strip() for line in lines if line])

        unwrapped_content = ""
        for line in content.split("\n\n"):
            # if a line contains more opening quote(「) than closing quote(」),
            # we're still within the same paragraph.
            # e.g.:
            # 「...」「...
            # 「...
            if line.count("「") > line.count("」"):
                unwrapped_content = unwrapped_content + line.strip()
            elif (
                re.search(r"[…。？！]{1}」?$", line)
                or re.search(r"」$", line)
                or re.match(r"^[ \t]*……[ \t]*$", line)
                or re.match(r"^「」$", line)
                or re.match(r".*[》：＊\*]$", line)
                or re.match(r".*[a-zA-Z0-9]$", line)
            ):
                unwrapped_content = unwrapped_content + line.strip() + "\n\n"
            elif re.match(RE_CHAPTER, line):
                # replace full-width space with half-wdith space.
                # looks nicer on the output.
                header = line.replace(IDEOGRAPHIC_SPACE * 2, SPACE).replace(
                    IDEOGRAPHIC_SPACE, SPACE
                )
                unwrapped_content = (
                    unwrapped_content + "\n\n" + header.strip() + "\n\n"
                )
            else:
                unwrapped_content = unwrapped_content + line.strip()

        return unwrapped_content

    def do_wrapping(self, content: str) -> str:
        """
        Wrapping and filling CJK text.
        """
        logger.info("Wrapping paragraph to width: {}", self.width)

        paragraphs = []
        # We don't remove empty line and keep all formatting as it.
        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()

            lines = cjkwrap.wrap(paragraph, width=self.width)
            paragraph = "\n".join(lines)
            paragraphs.append(paragraph)

        wrapped_content = "\n".join(paragraphs)
        return wrapped_content

    def parse_content(self, content: str) -> tuple:
        """
        Parse the content into volumes (if exists) and chapters.
        """
        volume_pattern = re.compile(RE_VOLUME, re.MULTILINE)
        volume_headers = re.findall(volume_pattern, content)

        volumes = []
        chapters = []

        if not volume_headers:
            logger.info("Found volumes: 0")
            (parsed_content, chapters) = self.parse_chapters(content)
            if parsed_content:
                logger.info("Found chapters: {}", len(parsed_content))
            else:
                logger.error("Found chapters: 0")
        else:
            logger.info("Found volumes: {}", len(volume_headers))
            volume_bodies = re.split(volume_pattern, content)
            parsed_volumes = list(zip(volume_headers, volume_bodies[1:]))

            parsed_content = []
            for volume_header, body in parsed_volumes:
                (parsed_body, chapters) = self.parse_chapters(body)
                if parsed_body:
                    parsed_content.append((volume_header, parsed_body))
                    volumes.append(
                        Volume(
                            title=volume_header,
                            raw_content=body,
                            chapters=chapters,
                        )
                    )
                else:
                    logger.error(
                        "Found 0 chapters for volume: {}", volume_header
                    )

        return (parsed_content, volumes, chapters)

    @staticmethod
    def parse_chapters(content: str) -> tuple:
        """
        Split the content of txt file into chapters by chapter regex.
        """
        regex = re.compile(RE_CHAPTER, re.MULTILINE)
        headers = re.findall(regex, content)

        if not headers:
            return (False, [])

        bodies = re.split(regex, content)
        parsed_chapters = list(zip(headers, bodies[1:]))

        chapters = []
        for title, body in parsed_chapters:
            title = title.rstrip()
            paragraphs = body.split("\n\n")
            chapters.append(
                Chapter(title=title, raw_content=body, paragraphs=paragraphs)
            )

        return (parsed_chapters, chapters)
