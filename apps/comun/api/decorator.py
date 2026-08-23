import inspect
import uuid
import warnings
from typing import Any, Callable, List, Optional, Sequence, Type, Union, overload

from injector import inject, is_decorated_with_inject
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.signature import is_async
from ninja.throttling import BaseThrottle
from ninja_extra import ControllerBase, ModelControllerBase, ModelSchemaConfig
from ninja_extra.constants import (
    API_CONTROLLER_INSTANCE,
    CONTROLLER_WATERMARK,
    THROTTLED_FUNCTION,
    THROTTLED_OBJECTS,
)
from ninja_extra.controllers.base import (
    APIController as NinjaExtraAPIController,
    ControllerClassType,
    T,
    compute_api_route_function,
)
from ninja_extra.controllers.model.schemas import ModelPagination
from ninja_extra.controllers.registry import controller_registry
from ninja_extra.controllers.route.route_functions import AsyncRouteFunction as NinjaExtraAsyncRouteFunction
from ninja_extra.helper import get_function_name
from ninja_extra.permissions import BasePermissionType
from ninja_extra.reflect import reflect
from ninja_extra.shortcuts import fail_silently
from ninja_schema.errors import ConfigError

from apps.comun.api.builder import ModelControllerBuilder
from apps.comun.api.config import ModelConfig
from apps.comun.api.route_functions import AsyncRouteFunction, RouteFunction


class APIController(NinjaExtraAPIController):  # noqa
    def __call__(self, cls: ControllerClassType) -> ControllerClassType:  # noqa
        self.auto_import = getattr(cls, "auto_import", self.auto_import)
        if not issubclass(cls, ControllerBase):
            # We force the cls to inherit from `ControllerBase` by creating another type.
            cls = type(cls.__name__, (ControllerBase, cls), {})  # type:ignore[assignment]

        if reflect.has_metadata(API_CONTROLLER_INSTANCE, cls):
            raise Exception("Controller is already decorated with @api_controller")

        reflect.define_metadata(API_CONTROLLER_INSTANCE, self, cls)
        reflect.define_metadata(CONTROLLER_WATERMARK, True, cls)

        assert isinstance(
            cls.throttling_classes, (list, tuple)
        ), f"Controller[{cls.__name__}].throttling_class must be a list or tuple"

        throttling_objects: Union[BaseThrottle, List[BaseThrottle], NOT_SET_TYPE] = NOT_SET

        if self.throttle is not NOT_SET:
            throttling_objects = self.throttle
        elif cls.throttling_classes:
            throttling_init_kwargs = cls.throttling_init_kwargs or {}
            throttling_objects = [item(**throttling_init_kwargs) for item in cls.throttling_classes]

        class_name = str(cls.__name__).lower().replace("controller", "")
        if not self.tags:
            self.tags = [class_name]

        self._controller_class = cls

        if issubclass(cls, ModelControllerBase):
            if cls.model and cls.model_config:
                raise ConfigError("ModelController class should not have both `model` and `model_config`")

            if cls.model_config:
                assert cls.service_type is not None, "service_type is required for BaseApiController"
                # if model_config is not provided, treat controller class as normal
                builder = ModelControllerBuilder(cls, self)
                builder.register_model_routes()
                if hasattr(cls, "service"):
                    warnings.warn(
                        "BaseApiController.service is deprecated. Use BaseApiController.service_type instead.",
                        DeprecationWarning,
                        stacklevel=2,
                    )

            # STARTS CUSTOM LOGIC
            if cls.model and not cls.model_config:
                assert cls.service_type is not None, "service_type is required for BaseApiController"
                cls.model_config = ModelConfig(
                    model=cls.model,
                    allowed_routes=cls.allowed_routes,
                    async_routes=cls.async_routes,
                    create_schema=cls.create_schema,
                    retrieve_schema=cls.retrieve_schema,
                    update_schema=cls.update_schema,
                    patch_schema=cls.patch_schema,
                    create_route_info=cls.create_route_info,
                    find_one_route_info=cls.find_one_route_info,
                    update_route_info=cls.update_route_info,
                    patch_route_info=cls.patch_route_info,
                    list_route_info=cls.list_route_info,
                    delete_route_info=cls.delete_route_info,
                    schema_config=ModelSchemaConfig(
                        exclude={
                            "id",
                            "deleted",
                            "deleted_by_cascade",
                            "created_at",
                            "updated_at",
                            "created_by",
                            "updated_by",
                        }
                    ),
                    create_response_schema=cls.create_response_schema,
                    update_response_schema=cls.update_response_schema,
                    patch_response_schema=cls.patch_response_schema,
                    delete_response_schema=cls.delete_response_schema,
                    pagination=cls.pagination if cls.pagination else ModelPagination(),
                )
                builder = ModelControllerBuilder(cls, self)
                builder.register_model_routes()
                if hasattr(cls, "service"):
                    warnings.warn(
                        "ModelControllerBase.service is deprecated. Use BaseApiController.service_type instead.",
                        DeprecationWarning,
                        stacklevel=2,
                    )
            # ENDS CUSTOM LOGIC

        compute_api_route_function(cls, self)

        for _, v in self._controller_class_route_functions.items():
            throttled_endpoint = v.as_view.__dict__.get(THROTTLED_FUNCTION)
            if v.route.route_params.throttle is NOT_SET:
                if throttled_endpoint or throttling_objects is not NOT_SET:
                    v.route.route_params.throttle = v.as_view.__dict__.get(
                        THROTTLED_OBJECTS, lambda: throttling_objects
                    )()

            self._add_operation_from_route_function(v)

        if not is_decorated_with_inject(cls.__init__):
            fail_silently(inject, constructor_or_class=cls)

        controller_registry.add_controller(cls)
        return cls

    def _add_operation_from_route_function(self, route_function: RouteFunction) -> None:
        """Method override with the only purpose to use out custom RouteFunction classes.

        Otherwise, the async auth verification doesn't work.
        """
        # converts route functions to Operation model
        if route_function.route.route_params.operation_id is None:
            controller_name = str(self.controller_class.__name__).lower().replace("controller", "")
            route_function.route.route_params.operation_id = (
                f"{controller_name}_{route_function.route.view_func.__name__}"
            )
            if self.use_unique_op_id:
                route_function.route.route_params.operation_id += f"_{uuid.uuid4().hex[:8]}"

        route_has_auth = self._route_function_has_auth(route_function)
        auth = route_function.route.route_params.auth if route_has_auth else self.auth
        is_async_auth = (
            self._is_async_auth(route_function.route.route_params.auth) if route_has_auth else self.has_auth_async
        )

        if (
            auth
            and is_async_auth
            and not isinstance(route_function, (AsyncRouteFunction, NinjaExtraAsyncRouteFunction))
        ):
            raise Exception(
                f"You are using a Controller level Asynchronous Authentication Class, "
                f"All controller endpoint must be `async`.\n"
                f"Controller={self.controller_class.__name__}, "
                f"endpoint={get_function_name(route_function.route.view_func)}"
            )
        data = route_function.route.route_params.dict()
        if not data.get("url_name"):
            data["url_name"] = get_function_name(route_function.route.view_func)
        route_function.operation = self.add_api_operation(view_func=route_function.as_view, **data)

    def _route_function_has_auth(self, route_function: RouteFunction) -> bool:
        return bool((route_function.route.route_params.auth is not NOT_SET))

    def _is_async_auth(self, auth) -> bool:
        auth_callbacks = isinstance(auth, Sequence) and auth or [auth]
        for _auth in auth_callbacks:
            if _auth is None:
                return True

            _call_back = _auth if inspect.isfunction(_auth) else _auth.__call__
            if is_async(_call_back):
                return True

        return False


@overload
def api_controller(
    prefix_or_class: Union[ControllerClassType, Type[T]],
) -> Union[Type[ControllerBase], Type[T]]:  # pragma: no cover
    ...


@overload
def api_controller(
    prefix_or_class: str = "",
    auth: Any = NOT_SET,
    throttle: Union[BaseThrottle, List[BaseThrottle], NOT_SET_TYPE] = NOT_SET,
    tags: Union[Optional[List[str]], str] = None,
    permissions: Optional[List[BasePermissionType]] = None,
    auto_import: bool = True,
    urls_namespace: Optional[str] = None,
    use_unique_op_id: bool = True,
) -> Callable[[Union[Type, Type[T]]], Union[Type[ControllerBase], Type[T]]]:  # pragma: no cover
    ...


def api_controller(  # noqa
    prefix_or_class: Union[str, ControllerClassType] = "",
    auth: Any = NOT_SET,
    throttle: Union[BaseThrottle, List[BaseThrottle], NOT_SET_TYPE] = NOT_SET,
    tags: Union[Optional[List[str]], str] = None,
    permissions: Optional[List[BasePermissionType]] = None,
    auto_import: bool = True,
    urls_namespace: Optional[str] = None,
    use_unique_op_id: bool = True,
) -> Union[ControllerClassType, Callable[[ControllerClassType], ControllerClassType]]:
    if isinstance(prefix_or_class, type):
        return APIController(
            prefix="",
            auth=auth,
            tags=tags,
            permissions=permissions,
            auto_import=auto_import,
            throttle=throttle,
            use_unique_op_id=use_unique_op_id,
            urls_namespace=urls_namespace,
        )(prefix_or_class)

    def _decorator(cls: ControllerClassType) -> ControllerClassType:
        return APIController(
            prefix=str(prefix_or_class),
            auth=auth,
            tags=tags,
            permissions=permissions,
            auto_import=auto_import,
            throttle=throttle,
            use_unique_op_id=use_unique_op_id,
            urls_namespace=urls_namespace,
        )(cls)

    return _decorator
