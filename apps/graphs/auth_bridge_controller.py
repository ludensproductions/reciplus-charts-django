"""Emisión de código de intercambio — solo para plataformas nativas
(Android/iOS/Desktop), que no comparten cookies con el navegador del sistema donde
se abre /graphs. La web usa sesión compartida real y no pasa por aquí — ver
reciplus-djangoninja apps.auth.api_controller.establish_session.
"""
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, http_post

from apps.graphs import consts as graphs_consts
from apps.graphs.auth import bearer_token
from apps.graphs.auth_bridge import AuthBridgeError, create_exchange_code, resolve_user_from_token


@api_controller("", tags=["Graphs"], auth=None)
class GraphsAuthBridgeController(ControllerBase):

    @http_post("/exchange-code", auth=None)
    def exchange_code(self, request):
        """Valida el JWT (header Authorization) y regresa un código opaco de un
        solo uso para pegar en la URL de /graphs — nunca el JWT en sí."""
        token = bearer_token(request)
        if not token:
            raise HttpError(401, graphs_consts.ERROR_NOT_AUTHENTICATED)
        try:
            user = resolve_user_from_token(token)
        except AuthBridgeError as exc:
            raise HttpError(401, str(exc))
        return {"code": create_exchange_code(user)}
