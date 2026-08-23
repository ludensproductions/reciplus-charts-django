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

from ..consts import (
    API_CREATE_DESCRIPTION,
    API_CREATE_SUMMARY,
    API_PATH,
    API_TAG,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
)
from ..filters import StudentFilter
from ..models import Student
from .schemas import (
    CreateSchemaOut,
    DeleteSchemaOut,
    PatchSchemaOut,
    StudentSchemaIn,
    StudentSchemaOut,
    UpdateSchemaOut,
)

# Important note:
# If the endpoint doesn't have an auth method assigned, then the user will be an anonymous user, for example:
# print(context_user.username=) -> ''
# print(context_user.is_anonymous=) -> True
# print(context_user.is_authenticated=) -> False
# print(context_user.is_superuser=) -> False


@api_controller(
    API_PATH,
    tags=[API_TAG],
    auth=JWTAuth(),
)
class StudentController(BaseApiController):
    """API controller for Student operations.

    Provides REST API endpoints for CRUD operations with JWT authentication,
    filtering, and pagination support.
    """

    model = Student
    allowed_routes = ["create", "find_one", "list", "update", "patch", "delete"]
    create_schema = StudentSchemaIn
    update_schema = StudentSchemaIn
    patch_schema = StudentSchemaIn
    create_response_schema = CreateSchemaOut
    retrieve_schema = StudentSchemaOut
    update_response_schema = UpdateSchemaOut
    patch_response_schema = PatchSchemaOut
    delete_response_schema = DeleteSchemaOut

    create_route_info = {
        "path": "/create",  # Custom path for create route
        "summary": API_CREATE_SUMMARY,
        "description": API_CREATE_DESCRIPTION,
        "permissions": [PERMISSION_ADD],
    }

    find_one_route_info: dict = {
        "auth": JWTAuth(),
    }

    list_route_info: dict = {
        "auth": None,
    }

    update_route_info: dict = {
        "auth": [JWTAuth(), SessionAuth(csrf=False)],
        "permissions": [PERMISSION_CHANGE],
    }

    patch_route_info = {
        "permissions": [PERMISSION_CHANGE],
    }

    delete_route_info = {
        "permissions": [PERMISSION_DELETE],
    }

    pre_save = UtilsClass.pre_save

    filterset_class = StudentFilter  # Only applies for the list route
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
            HTTPStatus.OK: StudentSchemaOut | None,
        },
    )  # Can also set a custom permission here sending the `permissions` parameter.
    async def random_Students(self, request):
        """Retrieves a random Student instance.

        In real scenarios there shouldn't exist an endpoint that fetches random resources.
        Unless it is explicitly required.

        Args:
            request: HTTP request object.

        Returns:
            Tuple of (status_code, data_dict) with random Student or None.
        """
        Students = await self.model.objects.order_by("?").afirst()
        if not Students:
            return Status(HTTPStatus.OK, None)
        result = StudentSchemaOut.from_orm(Students)
        return Status(HTTPStatus.OK, result.dict())
