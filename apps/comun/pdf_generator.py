import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

import httpx
import requests
from django.conf import settings
from django.contrib.staticfiles import finders
from django.db.models.fields.files import ImageFieldFile
from django.template.loader import render_to_string


@dataclass(frozen=True)
class PDFPage:
    """Class that represents a page of a PDF, containing the template name, the context, and optionally the assets and images that will be used to render that section."""

    template_name: str
    context: dict

    assets: Optional[dict[str, str]] = None
    images: Optional[dict[str, Union[str, bytes, ImageFieldFile]]] = None
    page_properties: Optional[dict] = None


class PDFGenerator:
    """Simple class that provides functions to generate PDF files from HTML."""

    def __init__(self, timeout=30):
        self.BASE_URL = settings.GOTENBERG_API_INTERNAL
        self.BASIC_AUTH_ENABLED = settings.GOTENBERG_API_ENABLE_BASIC_AUTH
        self.USERNAME = settings.GOTENBERG_API_BASIC_AUTH_USERNAME
        self.PASSWORD = settings.GOTENBERG_API_BASIC_AUTH_PASSWORD
        self.timeout = timeout
        self._async_client: httpx.AsyncClient | None = None

    def _ainit(self):
        if self._async_client is None:
            auth = None
            if self.BASIC_AUTH_ENABLED:
                auth = (self.USERNAME, self.PASSWORD)

            self._async_client = httpx.AsyncClient(
                timeout=self.timeout,
                auth=auth,
            )

    async def _aclose(self):
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def _render_template(self, template_name: str, context: dict) -> bytes:
        rendered_html = render_to_string(
            template_name=template_name,
            context=context,
        )
        return rendered_html.encode("utf-8")

    def _load_assets(self, assets: Optional[dict[str, str]] = None) -> dict[str, bytes]:
        assets_bytes: dict[str, bytes] = {}
        assets = assets or {}

        for name, static_asset_path in assets.items():
            asset_found = finders.find(static_asset_path)

            if not asset_found:
                raise FileNotFoundError(f"Static asset not found: {static_asset_path}")

            asset_path = Path(asset_found).absolute()
            assets_bytes[name] = asset_path.read_bytes()

        return assets_bytes

    def _load_images(self, images: dict[str, Union[str, bytes, ImageFieldFile]] | None) -> dict[str, bytes]:
        images = images or {}
        result: dict[str, bytes] = {}

        for name, source in images.items():
            if isinstance(source, bytes):
                result[name] = source
            elif isinstance(source, str):
                path = Path(source)
                if not path.exists():
                    raise FileNotFoundError(f"Image not found: {source}")
                result[name] = path.read_bytes()
            elif isinstance(source, ImageFieldFile):
                result[name] = source.read()
            else:
                raise TypeError(f"Invalid image source for {name}")

        return result

    def _html_to_pdf(
        self,
        html: bytes,
        assets: Optional[dict[str, bytes]] = None,
        images: Optional[dict[str, bytes]] = None,
        page_properties: Optional[dict] = None,
    ) -> bytes:
        files = [
            ("files", ("index.html", html, "text/html")),
        ]

        for name, content in (images or {}).items():
            files.append(("files", (name, content)))

        for name, content in (assets or {}).items():
            files.append(("files", (name, content)))

        auth = None

        if self.BASIC_AUTH_ENABLED:
            auth = (self.USERNAME, self.PASSWORD)

        resp = requests.post(
            f"{self.BASE_URL}/forms/chromium/convert/html",
            files=files,
            timeout=self.timeout,
            data=page_properties or {},
            auth=auth,
        )
        resp.raise_for_status()

        return resp.content

    def _merge_pdfs(self, pdfs: list[bytes]) -> bytes:
        """Method that merges multiple PDFs into a single PDF.

        Args:
            pdfs (list[bytes]): A list of PDFs as bytes.

        Returns:
            bytes: The merged PDF as bytes.
        """
        files = []

        for idx, pdf in enumerate(pdfs):
            files.append(("files", (f"pdf{idx}.pdf", pdf, "application/pdf")))

        auth = None
        if self.BASIC_AUTH_ENABLED:
            auth = (self.USERNAME, self.PASSWORD)

        resp = requests.post(
            f"{self.BASE_URL}/forms/pdfengines/merge",
            files=files,
            timeout=self.timeout,
            auth=auth,
        )
        resp.raise_for_status()

        return resp.content

    async def _async_html_to_pdf(
        self,
        html: bytes,
        assets: Optional[dict[str, bytes]] = None,
        images: Optional[dict[str, bytes]] = None,
        page_properties: Optional[dict] = None,
    ):
        files = [
            ("files", ("index.html", html, "text/html")),
        ]

        for name, content in (images or {}).items():
            files.append(("files", (name, content)))

        for name, content in (assets or {}).items():
            files.append(("files", (name, content)))

        resp = await self._async_client.post(
            f"{self.BASE_URL}/forms/chromium/convert/html",
            files=files,
            data=page_properties or {},
        )
        resp.raise_for_status()

        return resp.content

    async def _async_merge_pdfs(self, pdfs: list[bytes]) -> bytes:
        """Method that merges multiple PDFs into a single PDF.

        Args:
            pdfs (list[bytes]): A list of PDFs as bytes.

        Returns:
            bytes: The merged PDF as bytes.
        """
        files = []

        for idx, pdf in enumerate(pdfs):
            files.append(("files", (f"pdf{idx}.pdf", pdf, "application/pdf")))

        resp = await self._async_client.post(
            f"{self.BASE_URL}/forms/pdfengines/merge",
            files=files,
        )
        resp.raise_for_status()

        return resp.content

    def generate_pdf(
        self,
        template_name: str,
        context: dict,
        assets: Optional[dict[str, str]] = None,
        images: Optional[dict[str, Union[str, bytes, ImageFieldFile]]] = None,
        page_properties: Optional[dict] = None,
    ) -> str:
        """Method that generates a PDF from the template and context provided.

        Args:
            template_name (str): The template that will be used to generate the PDF.
            context (dict): The context needed to render the template provided.
            assets (Optional[dict[str, str]]): The assets that will be loaded when rendering the PDF. Defaults to None.
                And example could be:
                {
                    "styles.css": "assets/css/styles.css",
                }
            images (Optional[dict[str, Union[str, bytes, ImageFieldFile]]]): The images that will be loaded when rendering the PDF. Defaults to None.
                The key is the name that will be used to reference the image in the template, and the value can be a path to the image, the bytes of the image, or an ImageFieldFile. An example could be:
                {
                    "cover.jpg": "/path/to/cover.jpg",
                    "cover2.jpg": b"...bytes of the image...",
                    "cover3.jpg": <ImageFieldFile: cover3.jpg>,
                }
            page_properties(Optional[dict]): Additional properties related to the page setup, such as margins, orientation, etc. (not implemented in this example, but can be extended in the future). Defaults to None.
                For more information about page properties, please refer to: https://gotenberg.dev/docs/convert-with-chromium/convert-html-to-pdf#rendering-behavior

        Returns:
            str: The PDF as a base64 string.

        Raises:
            FileNotFoundError: Raised when the asset provided isn't found.
        """
        assets_bytes = self._load_assets(assets)
        html_bytes = self._render_template(template_name, context)
        images_bytes = self._load_images(images)

        pdf_bytes = self._html_to_pdf(
            html=html_bytes,
            assets=assets_bytes,
            images=images_bytes,
            page_properties=page_properties,
        )

        return base64.b64encode(pdf_bytes).decode()

    def generate_pdfs(
        self,
        sections: list[PDFPage],
        merge: bool = False,
    ) -> list[str] | str:
        """Method that generates multiple PDFs from the templates and contexts provided.

        Args:
            sections (list[PDFPage]): A list of sections, where each section contains a template name and a context that will be used to render the PDF.
            merge (bool): If True, it will merge all the sections into a single PDF. Defaults to False.
            page_properties(Optional[dict]): Additional properties related to the page setup, such as margins, orientation, etc. (not implemented in this example, but can be extended in the future). Defaults to None.
                For more information about page properties, please refer to: https://gotenberg.dev/docs/convert-with-chromium/convert-html-to-pdf#rendering-behavior

        Returns:
            list[str]: A list of generated PDFs as base64 strings.
            str: If merge is True, it will return a single PDF as a base64 string.
        """
        raw_results: list[bytes] = []

        for section in sections:
            assets_bytes = self._load_assets(section.assets)
            images_bytes = self._load_images(section.images)

            html_bytes = self._render_template(
                section.template_name,
                section.context,
            )

            pdf_bytes = self._html_to_pdf(
                html=html_bytes,
                assets=assets_bytes,
                images=images_bytes,
                page_properties=section.page_properties,
            )

            raw_results.append(pdf_bytes)

        if merge and len(raw_results) > 1:
            merged_pdf_bytes = self._merge_pdfs(raw_results)
            return base64.b64encode(merged_pdf_bytes).decode()
        elif merge and len(raw_results) == 1:
            return base64.b64encode(raw_results[0]).decode()

        return [base64.b64encode(pdf_bytes).decode() for pdf_bytes in raw_results]

    async def async_generate_pdf(
        self,
        template_name: str,
        context: dict,
        assets: Optional[dict[str, str]] = None,
        images: Optional[dict[str, Union[str, bytes, ImageFieldFile]]] = None,
        page_properties: Optional[dict] = None,
    ) -> str:
        """Method that generates a PDF from the template and context provided.

        This version is for asynchronous contexts, and it uses an async HTTP client to send the request to Gotenberg.

        Note:
            This method does not execute requests concurrently. Multiple PDF generations
            are processed sequentially. Its purpose is to avoid blocking the event loop,
            not to improve throughput.

        Args:
            template_name (str): The template that will be used to generate the PDF.
            context (dict): The context needed to render the template provided.
            assets (Optional[dict[str, str]]): The assets that will be loaded when rendering the PDF. Defaults to None.
                And example could be:
                {
                    "styles.css": "assets/css/styles.css",
                }
            images (Optional[dict[str, Union[str, bytes, ImageFieldFile]]]): The images that will be loaded when rendering the PDF. Defaults to None.
                The key is the name that will be used to reference the image in the template, and the value can be a path to the image, the bytes of the image, or an ImageFieldFile. An example could be:
                {
                    "cover.jpg": "/path/to/cover.jpg",
                    "cover2.jpg": b"...bytes of the image...",
                    "cover3.jpg": <ImageFieldFile: cover3.jpg>,
                }
            page_properties(Optional[dict]): Additional properties related to the page setup, such as margins, orientation, etc. (not implemented in this example, but can be extended in the future). Defaults to None.
                For more information about page properties, please refer to: https://gotenberg.dev/docs/convert-with-chromium/convert-html-to-pdf#rendering-behavior

        Returns:
            str: The PDF as a base64 string.

        Raises:
            FileNotFoundError: Raised when the asset provided isn't found.
        """
        assets_bytes = self._load_assets(assets)
        html_bytes = self._render_template(template_name, context)
        images_bytes = self._load_images(images)

        self._ainit()

        pdf_bytes = await self._async_html_to_pdf(
            html=html_bytes,
            assets=assets_bytes,
            images=images_bytes,
            page_properties=page_properties,
        )

        await self._aclose()

        return base64.b64encode(pdf_bytes).decode()

    async def async_generate_pdfs(
        self,
        sections: list[PDFPage],
        merge: bool = False,
    ) -> list[str] | str:
        """Method that generates multiple PDFs from the templates and contexts provided.

        Note:
            This method does not execute requests concurrently. Multiple PDF generations
            are processed sequentially. Its purpose is to avoid blocking the event loop,
            not to improve throughput.

        Args:
            sections (list[PDFPage]): A list of sections, where each section contains a template name and a context that will be used to render the PDF.
            merge (bool): If True, it will merge all the sections into a single PDF. Defaults to False.
            page_properties(Optional[dict]): Additional properties related to the page setup, such as margins, orientation, etc. (not implemented in this example, but can be extended in the future). Defaults to None.
                For more information about page properties, please refer to: https://gotenberg.dev/docs/convert-with-chromium/convert-html-to-pdf#rendering-behavior

        Returns:
            list[str]: A list of generated PDFs as base64 strings.
            str: If merge is True, it will return a single PDF as a base64 string.
        """
        raw_results: list[bytes] = []
        self._ainit()

        for section in sections:
            assets_bytes = self._load_assets(section.assets)
            images_bytes = self._load_images(section.images)

            html_bytes = self._render_template(
                section.template_name,
                section.context,
            )

            pdf_bytes = await self._async_html_to_pdf(
                html=html_bytes,
                assets=assets_bytes,
                images=images_bytes,
                page_properties=section.page_properties,
            )

            raw_results.append(pdf_bytes)

        if merge and len(raw_results) > 1:
            merged_pdf_bytes = await self._async_merge_pdfs(raw_results)
            await self._aclose()
            return base64.b64encode(merged_pdf_bytes).decode()
        elif merge and len(raw_results) == 1:
            await self._aclose()
            return base64.b64encode(raw_results[0]).decode()

        await self._aclose()

        return [base64.b64encode(pdf_bytes).decode() for pdf_bytes in raw_results]
