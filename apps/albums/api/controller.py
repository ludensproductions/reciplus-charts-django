from ninja_extra import http_get
from ninja_jwt.authentication import AsyncJWTAuth, JWTAuth

from apps.albums.api.schemas import AlbumSchemaOut
from apps.albums.api.service import AlbumService
from apps.albums.consts import PERMISSION_ADD, PERMISSION_CHANGE, PERMISSION_DELETE, PERMISSION_VIEW
from apps.albums.models import Album
from apps.comun.api.controller import BaseApiController
from apps.comun.api.decorator import api_controller
from apps.comun.custom_logic import UtilsClass


@api_controller(
    "/albums",
    tags=["Albums"],
    # auth=AsyncJWTAuth(),
)
class AlbumController(BaseApiController):  # noqa: D101
    model = Album

    retrieve_schema = AlbumSchemaOut

    async_routes = True

    create_route_info = {
        "permissions": [PERMISSION_ADD],
        "auth": AsyncJWTAuth(),  # To authenticate the user and obtain it from context
    }

    update_route_info = {
        "permissions": [PERMISSION_CHANGE],
        "auth": AsyncJWTAuth(),
    }

    list_route_info = {
        "permissions": [PERMISSION_VIEW],
        "auth": AsyncJWTAuth(),
    }

    delete_route_info = {
        "permissions": [PERMISSION_DELETE],
        "auth": AsyncJWTAuth(),
    }

    pre_save = UtilsClass.pre_save
    service_type = AlbumService

    @http_get(
        "/generate-album-report",
        auth=JWTAuth(),
    )
    def generate_album_report(self, request):
        """Example of generating a PDF report with a custom template and assets.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        """
        return self.service.generate_pdf_report()

    @http_get(
        "/async-generate-album-report",
        auth=AsyncJWTAuth(),
    )
    async def async_generate_album_report(self, request):
        """Example of generating a PDF report with a custom template and assets.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        """
        return await self.service.async_generate_pdf_report()

    @http_get(
        "/generate-album-cards",
        auth=JWTAuth(),
    )
    def generate_album_cards(self, request):
        """Example of generating a PDF report with a custom template and assets.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        """
        return self.service.generate_album_cards()

    @http_get(
        "/async-generate-album-cards",
        auth=AsyncJWTAuth(),
    )
    async def async_generate_album_cards(self, request):
        """Example of generating a PDF report with a custom template and assets.

        In real scenarios there shouldn't exist an endpoint that fetches random resources to generate a PDF.
        """
        return await self.service.async_generate_album_cards()
