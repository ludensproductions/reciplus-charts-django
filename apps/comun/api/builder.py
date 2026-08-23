import typing as t

from ninja_extra.constants import ROUTE_OBJECT
from ninja_extra.controllers.model.builder import (
    ModelControllerBuilder as NinjaExtraModelControllerBuilder,
)
from ninja_extra.reflect import reflect

from apps.comun.api.factory import (
    ModelAsyncEndpointFactory,
    ModelEndpointFactory,
)
from apps.comun.api.route_functions import (
    AsyncRouteFunction,
    RouteFunction,
)

if t.TYPE_CHECKING:
    from ninja_extra import ModelControllerBase
    from ninja_extra.controllers.route import Route


class ModelControllerBuilder(NinjaExtraModelControllerBuilder):  # noqa
    def __init__(
        self,
        base_cls: t.Type["ModelControllerBase"],
        api_controller_instance: t.Any,
    ) -> None:
        super().__init__(base_cls, api_controller_instance)

        self._create_response_schema = self._config.create_response_schema
        self._update_response_schema = self._config.update_response_schema
        self._patch_response_schema = self._config.patch_response_schema
        self._delete_response_schema = self._config.delete_response_schema

        del self._route_factory
        self._route_factory: ModelEndpointFactory = (
            ModelAsyncEndpointFactory() if base_cls.model_config.async_routes else ModelEndpointFactory()
        )

    def _add_to_controller(self, func: t.Callable) -> None:
        route_obj: "Route" = t.cast("Route", reflect.get_metadata_or_raise_exception(ROUTE_OBJECT, func))
        route_function: t.Union[RouteFunction, AsyncRouteFunction]
        if route_obj.is_async:
            route_function = AsyncRouteFunction(route_obj, api_controller=self._api_controller_instance)
        else:
            route_function = RouteFunction(route_obj, api_controller=self._api_controller_instance)
        self._api_controller_instance.add_controller_route_function(route_function)

    def _register_create_endpoint(self) -> None:
        kw = {
            "url_name": f"{self._model_name.lower()}-create",
            "description": f"Create {self._model_name} item",
            "summary": "Create an item",
        }
        kw.update(self._config.create_route_info)
        create_item = self._route_factory.create(
            schema_in=self._create_schema,  # type:ignore[arg-type]
            schema_out=self._create_response_schema or self._retrieve_schema,  # type:ignore[arg-type]
            **kw,  # type:ignore[arg-type]
        )

        self._add_to_controller(create_item.setup(self._base_cls))

    def _register_update_endpoint(self) -> None:
        _path = "/{%s:%s}" % (
            self._pk_type.__name__.lower(),
            self._model_pk_name,
        )
        kw = {
            "url_name": f"{self._model_name.lower()}-put",
            "description": f"""Update {self._model_name} item by {self._model_pk_name}""",
            "summary": "Update an item",
        }
        kw.update(self._config.update_route_info)

        update_item = self._route_factory.update(
            path=_path,
            lookup_param=self._model_pk_name,
            schema_in=self._update_schema,  # type:ignore[arg-type]
            schema_out=self._update_response_schema or self._retrieve_schema,  # type:ignore[arg-type]
            **kw,  # type:ignore[arg-type]
        )

        self._add_to_controller(update_item.setup(self._base_cls))

    def _register_patch_endpoint(self) -> None:
        _pk_type = self._pk_type
        _path = "/{%s:%s}" % (
            _pk_type.__name__.lower(),
            self._model_pk_name,
        )

        kw = {
            "url_name": f"{self._model_name.lower()}-patch",
            "description": f"""Patch {self._model_name} item by {self._model_pk_name}""",
            "summary": "Patch an item",
        }
        kw.update(self._config.patch_route_info)

        patch_item = self._route_factory.patch(
            path=_path,
            lookup_param=self._model_pk_name,
            schema_out=self._patch_response_schema or self._retrieve_schema,  # type:ignore[arg-type]
            schema_in=self._patch_schema,  # type:ignore[arg-type]
            **kw,  # type:ignore[arg-type]
        )

        self._add_to_controller(patch_item.setup(self._base_cls))

    def _register_delete_endpoint(self) -> None:
        _path = "/{%s:%s}" % (
            self._pk_type.__name__,
            self._model_pk_name,
        )
        kw = {
            "url_name": f"{self._model_name.lower()}-delete",
            "description": f"""Delete {self._model_name} item""",
            "summary": "Delete an item",
        }
        kw.update(self._config.delete_route_info)

        delete_item = self._route_factory.delete(
            path=_path,
            lookup_param=self._model_pk_name,
            schema_out=self._delete_response_schema or self._retrieve_schema,  # type:ignore[arg-type]
            **kw,  # type:ignore[arg-type]
        )

        self._add_to_controller(delete_item.setup(self._base_cls))
