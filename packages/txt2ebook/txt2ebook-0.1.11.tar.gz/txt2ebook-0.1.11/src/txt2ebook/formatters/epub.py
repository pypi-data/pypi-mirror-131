"""
Module for generating epub file.
"""
import sys
import uuid
from pathlib import Path
from typing import Optional

from ebooklib import epub
from loguru import logger

from ..models import Book, Volume, Chapter

EPUB_TEMPLATE_PATH = Path(Path(__file__).parent.parent, "templates", "epub")
SPACE = "\u0020"


class EpubWriter:
    """
    Module for writing ebook in epub format.
    """

    def __init__(self, book: Book, opts: dict) -> None:
        self.book = book
        self.content = book.parsed_content
        self.input_file = opts["input_file"]
        self.output_file = opts["output_file"]
        self.template = opts["epub_template"]

    def write(self) -> None:
        """
        Optionally backup and overwrite the txt file.
        """
        book = epub.EpubBook()

        if self.book.title:
            book.set_title(self.book.title)
            book.set_identifier(self._gen_id())

        if self.book.language:
            book.set_language(self.book.language)

        if self.book.authors:
            book.add_author(", ".join(self.book.authors))

        if self.book.cover:
            with open(self.book.cover, "rb") as image:
                book.set_cover("cover.jpg", image.read(), False)

                cover_page = self._build_cover()
                book.add_item(cover_page)
                book.toc.append(cover_page)
                book.spine.append(cover_page)

        self._build_nav(book)

        if self.book.volumes:
            logger.debug("Generate {} EPUB volumes", len(self.book.volumes))

            for volume in self.book.volumes:
                html_chapters = []
                for chapter in volume.chapters:
                    html_chapter = self._build_chapter(chapter, volume)
                    book.add_item(html_chapter)
                    book.spine.append(html_chapter)
                    html_chapters.append(html_chapter)

                book.toc.append((epub.Section(volume.title), html_chapters))
        else:
            logger.debug("Generate {} EPUB chapters", len(self.book.chapters))

            for chapter in self.book.chapters:
                html_chapter = self._build_chapter(chapter)
                book.add_item(html_chapter)
                book.spine.append(html_chapter)
                book.toc.append(html_chapter)

        output_filename = self._gen_output_filename()
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(output_filename, book, {})
        logger.info("Generate EPUB file: {}", output_filename)

    def _build_nav(self, book: epub.EpubBook) -> None:
        book.add_item(epub.EpubNcx())

        try:
            logger.info("EPUB CSS template: {}", self.template)
            css_file = Path(EPUB_TEMPLATE_PATH, self.template + ".css")
            with open(css_file, "r") as css:
                book_css = epub.EpubItem(
                    uid="style_nav",
                    file_name="style/book.css",
                    media_type="text/css",
                    content=css.read(),
                )
                book.add_item(book_css)

                nav = epub.EpubNav()
                nav.add_link(
                    href="style/book.css", rel="stylesheet", type="text/css"
                )
                book.add_item(nav)
                book.spine.append("nav")
        except FileNotFoundError:
            logger.error("Unknown EPUB template name: {}", self.template)
            sys.exit(0)

    def _gen_id(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, self.book.title))

    def _gen_output_filename(self) -> Path:
        """
        Determine the output EPUB filename.
        """
        return Path(
            self.output_file
            or Path(self.book.title or self.input_file).stem + ".epub"
        )

    def _build_cover(self) -> epub.EpubHtml:
        html = """
            <div id="cover"">
                <img src="cover.jpg" alt="cover" />
            </div>
        """
        cover = epub.EpubHtml(
            title=self.book.structure_names["cover"],
            file_name="cover.xhtml",
            lang=self.book.language,
            content=html,
        )
        cover.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )
        return cover

    def _build_chapter(
        self, chapter: Chapter, volume: Optional[Volume] = None
    ) -> epub.EpubHtml:
        """
        Generates the whole chapter to HTML.
        """
        if volume:
            filename = f"{volume.title}_{chapter.title}"
        else:
            filename = chapter.title

        filename = filename.replace(SPACE, "_")

        html = f"<h2>{chapter.title}</h2>"
        for paragraph in chapter.paragraphs:
            paragraph = paragraph.replace(SPACE, "").replace("\n", "")
            html = html + f"<p>{paragraph}</p>"

        epub_html = epub.EpubHtml(
            title=chapter.title,
            file_name=filename + ".xhtml",
            lang=self.book.language,
            content=html,
        )
        epub_html.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )

        return epub_html
