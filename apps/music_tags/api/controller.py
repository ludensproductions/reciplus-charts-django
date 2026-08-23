from http import HTTPStatus

from ninja.responses import Status
from ninja.security import SessionAuth
from ninja_extra import http_get, http_post
from ninja_jwt.authentication import AsyncJWTAuth, JWTAuth

from apps.comun.api.controller import BaseApiController
from apps.comun.api.decorator import api_controller
from apps.music_tags.consts import PERMISSION_ADD, PERMISSION_VIEW
from apps.music_tags.models import MusicTags

from .filters import MusicTagsFilterSet
from .schemas import EchoSchemaIn, EchoSchemaOut, MusicTagsSchemaOut
from .service import MusicTagsService


@api_controller(
    "/music-tags",
    tags=["Music Tags"],
    auth=AsyncJWTAuth(),
    permissions=[
        PERMISSION_VIEW,
    ],
)
class MusicTagsController(BaseApiController):
    """Controller básico para MusicTags."""

    model = MusicTags
    async_routes = True
    retrieve_schema = MusicTagsSchemaOut

    create_route_info = {
        "permissions": [
            PERMISSION_ADD,
        ],
    }

    filterset_class = MusicTagsFilterSet
    service_type = MusicTagsService

    @http_get(
        "random/",
        auth=[JWTAuth(), SessionAuth()],
        response={
            HTTPStatus.OK: MusicTagsSchemaOut,
            HTTPStatus.NOT_FOUND: None,
        },
    )
    def get_random_music_tag(self, request):
        """Test endpoint.

        In real scenarios there shouldn't exist an endpoint that fetches random resources.
        Unless it is explicitly required.
        """
        return self.service.get_random_music_tag()

    @http_post(
        "echo/",
        auth=JWTAuth(),
        response={
            HTTPStatus.OK: EchoSchemaOut,
        },
    )
    def echo(self, request, payload: EchoSchemaIn):
        """Test endpoint."""
        return Status(HTTPStatus.OK, EchoSchemaOut(echo=payload.text))
