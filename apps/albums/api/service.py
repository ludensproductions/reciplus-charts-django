from http import HTTPStatus
from pathlib import Path

from ninja.responses import Status

from apps.albums.api.consts import (
    ALBUM_CARDS_ASSETS,
    ALBUM_REPORT_ASSETS,
    ALBUMS_CARDS_TEMPLATE,
    ALBUMS_REPORT_TEMPLATE,
    BASE_PDF_PAGE_PROPERTIES,
)
from apps.comun.api.service import GenericModelService
from apps.comun.pdf_generator import PDFGenerator, PDFPage


class AlbumService(GenericModelService):  # noqa
    def get_all(self, **kwargs):  # noqa
        qs = super().get_all(**kwargs)
        qs = qs.order_by("title")
        return qs

    def generate_pdf_report(
        self,
    ):
        """Method to generate one PDF report.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        Unless it is explicitly required.
        """
        albums = list(self.model.objects.order_by("?")[:4])

        if not albums:
            return Status(HTTPStatus.NOT_FOUND, None)

        images = {Path(album.cover.name).name: album.cover.path for album in albums if album.cover}

        generator = PDFGenerator()
        pdf_base64 = generator.generate_pdf(
            template_name=ALBUMS_REPORT_TEMPLATE,
            context={
                "albums": albums,
            },
            assets=ALBUM_REPORT_ASSETS,
            images=images,
        )

        return Status(HTTPStatus.OK, {"content": pdf_base64})

    async def async_generate_pdf_report(
        self,
    ):
        """Method to generate one PDF report asynchronously.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        Unless it is explicitly required.
        """
        albums = self.model.objects.order_by("?")[:4]

        if not await albums.aexists():
            return Status(HTTPStatus.NOT_FOUND, None)

        albums_list = []
        images = {}

        async for album in albums:
            albums_list.append(album)
            if album.cover:
                images[Path(album.cover.name).name] = album.cover.path

        generator = PDFGenerator()
        pdf_base64 = await generator.async_generate_pdf(
            template_name=ALBUMS_REPORT_TEMPLATE,
            context={
                "albums": albums_list,
            },
            assets=ALBUM_REPORT_ASSETS,
            images=images,
        )

        return Status(HTTPStatus.OK, {"content": pdf_base64})

    def generate_album_cards(
        self,
    ):
        """Method to generate PDF albums cards.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        Unless it is explicitly required.
        """
        albums = list(self.model.objects.order_by("?")[:4].prefetch_related("songs"))

        if not albums:
            return Status(HTTPStatus.NOT_FOUND, None)

        sections = []

        for album in albums:
            images = {Path(album.cover.name).name: album.cover.path} if album.cover else None

            sections.append(
                PDFPage(
                    template_name=ALBUMS_CARDS_TEMPLATE,
                    context={"album": album, "songs": album.songs.all()},
                    assets=ALBUM_CARDS_ASSETS,
                    images=images,
                    page_properties=BASE_PDF_PAGE_PROPERTIES,
                )
            )

        generator = PDFGenerator()
        pdf_base64 = generator.generate_pdfs(sections=sections, merge=True)

        return Status(HTTPStatus.OK, {"content": pdf_base64})

    async def async_generate_album_cards(
        self,
    ):
        """Method to generate PDF albums cards asynchronously.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        Unless it is explicitly required.
        """
        albums = self.model.objects.order_by("?")[:4].prefetch_related("songs")

        if not await albums.aexists():
            return Status(HTTPStatus.NOT_FOUND, None)

        sections = []

        async for album in albums:
            images = {Path(album.cover.name).name: album.cover.path} if album.cover else None

            songs = [song async for song in album.songs.all()]

            sections.append(
                PDFPage(
                    template_name=ALBUMS_CARDS_TEMPLATE,
                    context={"album": album, "songs": songs},
                    assets=ALBUM_CARDS_ASSETS,
                    images=images,
                    page_properties=BASE_PDF_PAGE_PROPERTIES,
                )
            )

        generator = PDFGenerator()
        pdf_base64 = await generator.async_generate_pdfs(sections=sections, merge=True)

        return Status(HTTPStatus.OK, {"content": pdf_base64})
