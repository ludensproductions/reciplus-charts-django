from typing import Any, Callable, Optional, cast

from django.http import HttpRequest, HttpResponse
from ninja_extra.context import (
    RouteContext,
    get_route_execution_context,
)
from ninja_extra.controllers.route.route_functions import RouteFunction as NinjaExtraRouteFunction
from ninja_extra.dependency_resolver import get_injector, service_resolver


class RouteFunction(NinjaExtraRouteFunction):  # noqa
    def _get_controller_instance(self):
        from .controller import BaseApiController

        injector = get_injector()
        additional_kwargs = {}

        if issubclass(self.api_controller.controller_class, BaseApiController):
            controller_klass = cast(BaseApiController, self.api_controller.controller_class)
            # make sure model_config is not None
            if controller_klass.model_config is not None:
                service = injector.create_object(
                    controller_klass.service_type,
                    additional_kwargs={
                        "model": controller_klass.model_config.model,
                        "pre_save": controller_klass.pre_save,
                        "post_save": controller_klass.post_save,
                        "filterset_class": controller_klass.filterset_class,
                    },
                )
                additional_kwargs.update({"service": service})

        controller_instance = injector.create_object(
            self.api_controller.controller_class, additional_kwargs=additional_kwargs
        )

        return controller_instance


class AsyncRouteFunction(RouteFunction):  # noqa
    async def async_run_check_permissions(self, route_context: RouteContext) -> None:  # noqa
        from asgiref.sync import sync_to_async

        _route_context = route_context or cast(RouteContext, service_resolver(RouteContext))
        with self._prep_controller_route_execution(_route_context) as ctx:
            # Use async_check_permissions if available, otherwise use sync_to_async
            if hasattr(ctx.controller_instance, "async_check_permissions"):
                await ctx.controller_instance.async_check_permissions()
            else:
                await sync_to_async(ctx.controller_instance.check_permissions)()

    def get_view_function(self) -> Callable:  # noqa
        async def as_view(
            request: HttpRequest,
            route_context: Optional[RouteContext] = None,
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            _route_context = route_context or cast(RouteContext, service_resolver(RouteContext))
            with self._prep_controller_route_execution(_route_context, **kwargs) as ctx:
                # await sync_to_async(ctx.controller_instance.check_permissions)()
                result = await self.route.view_func(ctx.controller_instance, *args, **ctx.view_func_kwargs)
            return result

        as_view.get_route_function = lambda: self  # type:ignore
        return as_view

    def __repr__(self) -> str:  # pragma: no cover # noqa
        if not self.api_controller:
            return f"<AsyncRouteFunction, controller: No Controller Found, path: {self.__str__()}>"
        return f"<AsyncRouteFunction, controller: {self.api_controller.controller_class.__name__}, path: {self.__str__()}>"

    async def __call__(  # noqa
        self,
        request: HttpRequest,
        temporal_response: Optional[HttpResponse] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        context = get_route_execution_context(
            request,
            temporal_response,
            self.route.permissions or self.api_controller.permission_classes,  # type:ignore[arg-type]
            *args,
            **kwargs,
        )
        await self.async_run_check_permissions(context)
        return await self.as_view(request, *args, route_context=context, **kwargs)
