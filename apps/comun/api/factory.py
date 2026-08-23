"""Factories to generate sync and async CRUD endpoints for Ninja Extra controllers."""

import typing as t

from django.db.models import Model as DjangoModel, QuerySet
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.params import Body
from ninja.throttling import BaseThrottle
from ninja_extra import status
from ninja_extra.controllers.model.endpoints import (
    ModelEndpointFactory as NinjaExtraModelEndpointFactory,
    ModelEndpointFunction,
    _check_if_coroutine,
)
from ninja_extra.exceptions import NotFound
from ninja_extra.permissions import BasePermission
from pydantic import BaseModel as PydanticModel

from apps.comun.consts import SUCCESS_ITEM_DELETED

if t.TYPE_CHECKING:
    from ninja_extra.controllers.base import ModelControllerBase


class ModelEndpointFactory(NinjaExtraModelEndpointFactory):
    """Factory for creating CRUD operations of a model controller and for adding custom route functions to controllers.

    Example:
    ```python

    api_controller
    class SampleModelController(ModelControllerBase):

        create_sample = ModelEndpointFactory.create()
        update_sample = ModelEndpointFactory.update()

        delete_sample = ModelEndpointFactory.delete()
        patch_sample = ModelEndpointFactory.patch()

        get_sample = ModelEndpointFactory.get()
        list_samples = ModelEndpointFactory.list()
    ```
    """

    @classmethod
    def delete(
        cls,
        path: str,
        lookup_param: str,
        schema_out: t.Type[PydanticModel],
        status_code: int = status.HTTP_200_OK,
        auth: t.Any = NOT_SET,
        throttle: t.Union[BaseThrottle, t.List[BaseThrottle], NOT_SET_TYPE] = NOT_SET,
        response: t.Any = NOT_SET,
        url_name: t.Optional[str] = None,
        description: t.Optional[str] = None,
        object_getter: t.Optional[t.Callable[..., DjangoModel]] = None,
        custom_handler: t.Optional[t.Callable[..., t.Any]] = None,
        operation_id: t.Optional[str] = None,
        summary: t.Optional[str] = "Delete An Item",
        tags: t.Optional[t.List[str]] = None,
        deprecated: t.Optional[bool] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        include_in_schema: bool = True,
        permissions: t.Optional[t.List[t.Union[t.Type[BasePermission], BasePermission, t.Any]]] = None,
        openapi_extra: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ModelEndpointFunction:
        """Creates a DELETE Action to list Items."""
        return super().delete(
            path=path,
            lookup_param=lookup_param,
            status_code=status_code,
            auth=auth,
            throttle=throttle,
            response=response if response is not NOT_SET else {status_code: schema_out},
            url_name=url_name,
            description=description,
            object_getter=object_getter,
            custom_handler=custom_handler,
            operation_id=operation_id,
            summary=summary,
            tags=tags,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            include_in_schema=include_in_schema,
            permissions=permissions,
            openapi_extra=openapi_extra,
        )

    @classmethod
    def _delete_handler(
        cls,
        *,
        object_getter: t.Optional[t.Callable[..., DjangoModel]],
        lookup_param: str,
        custom_handler: t.Optional[t.Callable[..., t.Any]],
        status_code: int,
    ) -> t.Callable:
        """Build the delete handler used by generated DELETE endpoints.

        Args:
            object_getter (Optional[Callable[..., DjangoModel]]): Optional
                callable used to retrieve the target object.
            lookup_param (str): URL kwarg name that contains the object id.
            custom_handler (Optional[Callable[..., Any]]): Optional custom
                delete implementation.
            status_code (int): HTTP status code used for successful responses.

        Returns:
            Callable: Configured delete endpoint function.
        """

        def delete_item(self: "ModelControllerBase", **kwargs: t.Any) -> t.Any:
            """Delete one item and return either service output or fallback payload."""
            pk = kwargs.pop(lookup_param)
            obj = object_getter(self, pk=pk, **kwargs) if object_getter else self.service.get_one(pk=pk, **kwargs)
            if not obj:  # pragma: no cover
                raise NotFound()
            self.check_object_permissions(obj)

            instance = (
                custom_handler(self, instance=obj, **kwargs)
                if custom_handler
                else self.service.delete(instance=obj, **kwargs)
            )

            if not instance:
                return self.create_response(message={"message": SUCCESS_ITEM_DELETED}, status_code=status_code)

            return instance

        delete_item.__name__ = cls._change_name("delete_item")
        return delete_item


class ModelAsyncEndpointFactory(ModelEndpointFactory):
    """Factory for creating asynchronous CRUD operations of a model controller and for adding custom asynchronous route functions to controllers.

    Example:
    ```python

    api_controller
    class SampleModelController(ModelControllerBase):

        create_sample = ModelAsyncEndpointFactory.create()
        update_sample = ModelAsyncEndpointFactory.update()

        delete_sample = ModelAsyncEndpointFactory.delete()
        patch_sample = ModelAsyncEndpointFactory.patch()

        get_sample = ModelAsyncEndpointFactory.get()
        list_samples = ModelAsyncEndpointFactory.list()
    ```
    """

    @classmethod
    def _list_handler(cls, *, queryset_getter: t.Optional[t.Callable[..., QuerySet]]) -> t.Callable:
        """Build the asynchronous list handler for generated endpoints.

        Args:
            queryset_getter (Optional[Callable[..., QuerySet]]): Optional
                callable that returns the queryset source.

        Returns:
            Callable: Configured async list endpoint function.
        """

        async def list_items(self: "ModelControllerBase", **kwargs: t.Any) -> t.Any:
            """List Items of testing."""
            if queryset_getter:
                res = queryset_getter(self, **kwargs)
            else:
                res = self.service.get_all_async(**kwargs)  # type:ignore[assignment]

            return await _check_if_coroutine(res)

        list_items.__name__ = cls._change_name("list_items")
        return list_items

    @classmethod
    def _delete_handler(
        cls,
        *,
        object_getter: t.Optional[t.Callable[..., DjangoModel]],
        lookup_param: str,
        custom_handler: t.Optional[t.Callable[..., t.Any]],
        status_code: int,
    ) -> t.Callable:
        """Build the asynchronous delete handler for generated endpoints.

        Args:
            object_getter (Optional[Callable[..., DjangoModel]]): Optional
                callable used to retrieve the target object.
            lookup_param (str): URL kwarg name that contains the object id.
            custom_handler (Optional[Callable[..., Any]]): Optional custom
                delete implementation.
            status_code (int): HTTP status code used for successful responses.

        Returns:
            Callable: Configured async delete endpoint function.
        """

        async def delete_item(self: "ModelControllerBase", **kwargs: t.Any) -> t.Any:
            """Delete one item asynchronously and return the resulting payload."""
            pk = kwargs.pop(lookup_param)
            obj = (
                object_getter(self, pk=pk, **kwargs) if object_getter else self.service.get_one_async(pk=pk, **kwargs)
            )
            obj = await _check_if_coroutine(obj)
            if not obj:  # pragma: no cover
                raise NotFound()
            self.check_object_permissions(obj)

            res = (
                custom_handler(self, instance=obj, **kwargs)
                if custom_handler
                else self.service.delete_async(instance=obj, **kwargs)  # type:ignore[arg-type]
            )

            res = await _check_if_coroutine(res)
            if not res:
                return self.create_response(message={"message": SUCCESS_ITEM_DELETED}, status_code=status_code)

            return res

        delete_item.__name__ = cls._change_name("delete_item")
        return delete_item

    @classmethod
    def _find_one_handler(
        cls,
        *,
        object_getter: t.Optional[t.Callable[..., DjangoModel]],
        lookup_param: str,
    ) -> t.Callable:
        """Build the asynchronous find-one handler for generated endpoints.

        Args:
            object_getter (Optional[Callable[..., DjangoModel]]): Optional
                callable used to fetch the object.
            lookup_param (str): URL kwarg name that contains the object id.

        Returns:
            Callable: Configured async get endpoint function.
        """

        async def get_item(self: "ModelControllerBase", **kwargs: t.Any) -> t.Any:
            """Fetch one item asynchronously and enforce object permissions."""
            pk = kwargs.pop(lookup_param)
            obj = (
                object_getter(self, pk=pk, **kwargs) if object_getter else self.service.get_one_async(pk=pk, **kwargs)
            )
            obj = await _check_if_coroutine(obj)

            if not obj:  # pragma: no cover
                raise NotFound()

            self.check_object_permissions(obj)
            return obj

        get_item.__name__ = cls._change_name("get_item")
        return get_item

    @classmethod
    def _patch_handler(
        cls,
        *,
        schema_in: t.Type[PydanticModel],
        object_getter: t.Optional[t.Callable[..., DjangoModel]],
        lookup_param: str,
        custom_handler: t.Optional[t.Callable[..., t.Any]],
    ) -> t.Callable:
        """Build the asynchronous PATCH handler for generated endpoints.

        Args:
            schema_in (Type[PydanticModel]): Input schema used for patch data.
            object_getter (Optional[Callable[..., DjangoModel]]): Optional
                callable used to fetch the object.
            lookup_param (str): URL kwarg name that contains the object id.
            custom_handler (Optional[Callable[..., Any]]): Optional custom
                patch implementation.

        Returns:
            Callable: Configured async patch endpoint function.
        """

        async def patch_item(
            self: "ModelControllerBase",
            data: schema_in = Body(default=...),  # type:ignore[valid-type]
            **kwargs: t.Any,
        ) -> t.Any:
            """Patch one item asynchronously and return the updated instance."""
            pk = kwargs.pop(lookup_param)
            obj = (
                object_getter(self, pk=pk, **kwargs) if object_getter else self.service.get_one_async(pk=pk, **kwargs)
            )
            obj = await _check_if_coroutine(obj)

            if not obj:  # pragma: no cover
                raise NotFound()
            self.check_object_permissions(obj)

            instance = (
                custom_handler(self, instance=obj, schema=data, **kwargs)
                if custom_handler
                else self.service.patch_async(instance=obj, schema=data, **kwargs)  # type:ignore[arg-type]
            )
            instance = await _check_if_coroutine(instance)

            assert instance, "`service.patch_async()` or `custom_handler` must return a value"
            return instance

        patch_item.__name__ = cls._change_name("patch_item")
        return patch_item

    @classmethod
    def _update_handler(
        cls,
        *,
        schema_in: t.Type[PydanticModel],
        object_getter: t.Optional[t.Callable[..., DjangoModel]],
        lookup_param: str,
        custom_handler: t.Optional[t.Callable[..., t.Any]],
    ) -> t.Callable:
        """Build the asynchronous PUT handler for generated endpoints.

        Args:
            schema_in (Type[PydanticModel]): Input schema used for update data.
            object_getter (Optional[Callable[..., DjangoModel]]): Optional
                callable used to fetch the object.
            lookup_param (str): URL kwarg name that contains the object id.
            custom_handler (Optional[Callable[..., Any]]): Optional custom
                update implementation.

        Returns:
            Callable: Configured async update endpoint function.
        """

        async def update_item(
            self: "ModelControllerBase",
            data: schema_in = Body(default=...),  # type:ignore[valid-type]
            **kwargs: t.Any,
        ) -> t.Any:
            """Update one item asynchronously and return the updated instance."""
            pk = kwargs.pop(lookup_param)
            obj = (
                object_getter(self, pk=pk, **kwargs) if object_getter else self.service.get_one_async(pk=pk, **kwargs)
            )
            obj = await _check_if_coroutine(obj)

            if not obj:  # pragma: no cover
                raise NotFound()

            self.check_object_permissions(obj)
            instance = (
                custom_handler(self, instance=obj, schema=data, **kwargs)
                if custom_handler
                else self.service.update_async(instance=obj, schema=data, **kwargs)  # type:ignore[arg-type]
            )
            instance = await _check_if_coroutine(instance)

            assert instance, "`service.update_async` or `custom_handler` must return a value"
            return instance

        update_item.__name__ = cls._change_name("update_item")
        return update_item

    @classmethod
    def _create_handler(
        cls,
        *,
        schema_in: t.Type[PydanticModel],
        custom_handler: t.Optional[t.Callable[..., t.Any]],
    ) -> t.Callable:
        """Build the asynchronous create handler for generated endpoints.

        Args:
            schema_in (Type[PydanticModel]): Input schema used for create data.
            custom_handler (Optional[Callable[..., Any]]): Optional custom
                create implementation.

        Returns:
            Callable: Configured async create endpoint function.
        """

        async def create_item(
            self: "ModelControllerBase",
            data: schema_in = Body(default=...),  # type:ignore[valid-type]
            **kwargs: t.Any,
        ) -> t.Any:
            """Create one item asynchronously and return the created instance."""
            instance = (
                custom_handler(self, data, **kwargs) if custom_handler else self.service.create_async(data, **kwargs)
            )
            instance = await _check_if_coroutine(instance)

            assert instance, "`service.create_async` or  `custom_handler` must return a value"
            return instance

        create_item.__name__ = cls._change_name("create_item")
        return create_item
