from http import HTTPStatus

from ninja.pagination import LimitOffsetPagination
from ninja.responses import Status
from ninja.security.session import SessionAuth
from ninja_extra import ModelPagination, http_get
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_jwt.authentication import JWTAuth

from apps.comun.api.controller import BaseApiController
from apps.comun.api.decorator import api_controller
from apps.comun.custom_logic import UtilsClass
from apps.movies.api.filters import MovieFilterSet
from apps.movies.api.schemas import (
    CreateSchemaOut,
    DeleteSchemaOut,
    MovieSchemaIn,
    MovieSchemaOut,
    PatchSchemaOut,
    UpdateSchemaOut,
)
from apps.movies.models import Movie

# Important note:
# If the endpoint doesn't have an auth method assigned, then the user will be an anonymous user, for example:
# print(f"{context_user.username=}") -> ''
# print(f"{context_user.is_anonymous=}") -> True
# print(f"{context_user.is_authenticated=}") -> False
# print(f"{context_user.is_superuser=}") -> False


@api_controller(
    "/movies",
    tags=["Movies"],
    auth=JWTAuth(),
)
class MovieController(BaseApiController):  # noqa
    model = Movie
    create_schema = MovieSchemaIn
    update_schema = MovieSchemaIn
    patch_schema = MovieSchemaIn
    retrieve_schema = MovieSchemaOut
    allowed_routes = ["create", "find_one", "update", "patch", "delete", "list"]

    create_route_info = {
        "path": "/create",  # Custom path for create route
        "summary": "Create a new movie",
        "description": "Create a new movie",
        "permissions": ["movies.add_movie"],
    }

    find_one_route_info: dict = {
        "auth": JWTAuth(),
    }
    update_route_info: dict = {
        "auth": [JWTAuth(), SessionAuth(csrf=False)],
        "permissions": ["movies.change_movie"],
    }
    patch_route_info = {"permissions": ["movies.change_movie"]}
    list_route_info: dict = {
        "auth": None,
    }
    delete_route_info = {"permissions": ["movies.delete_movie"]}

    create_response_schema = CreateSchemaOut
    update_response_schema = UpdateSchemaOut
    patch_response_schema = PatchSchemaOut
    delete_response_schema = DeleteSchemaOut

    pre_save = UtilsClass.pre_save

    filterset_class = MovieFilterSet  # Only applies for the list route

    # For a little more information on pagination see:
    # https://eadwincode.github.io/django-ninja-extra/api_controller/model_controller/02_model_configuration/#pagination-configuration
    pagination = ModelPagination(  # pagination must be an instance, not just the class
        klass=LimitOffsetPagination,
        pagination_schema=NinjaPaginationResponseSchema,
        paginator_kwargs={"limit": 20, "offset": 100},
    )

    @http_get(
        "/random",
        auth=None,
        response={
            HTTPStatus.OK: MovieSchemaOut | None,
        },
    )  # Can also set a custom permission here sending the `permissions` parameter.
    async def random_movie(self, request):
        """In real scenarios there shouldn't exist an endpoint that fetches random resources.

        Unless it is explicitly required.
        """
        movie = await self.model.objects.order_by("?").afirst()
        if not movie:
            return Status(HTTPStatus.OK, None)
        result = MovieSchemaOut.from_orm(movie)
        return Status(HTTPStatus.OK, result.dict())
