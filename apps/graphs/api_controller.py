"""Endpoints de datos de gráficas — requieren sesión ya establecida.

El intercambio de credencial (JWT -> sesión) vive aparte, en
apps.graphs.auth_bridge_controller.
"""
from datetime import date

from ninja_extra import ControllerBase, api_controller, http_get

from apps.graphs.auth import session_doctor_scope
from apps.graphs.service import GraphsService


@api_controller("", tags=["Graphs"], auth=None)
class GraphsController(ControllerBase):
    service = GraphsService()

    @http_get("/profits-and-losses", auth=None)
    def profits_and_losses(self, request, date_from: str | None = None, date_to: str | None = None):
        doctor_user_id = session_doctor_scope(request)
        parsed_from = date.fromisoformat(date_from) if date_from else None
        parsed_to = date.fromisoformat(date_to) if date_to else None
        return self.service.get_profits_and_losses(doctor_user_id=doctor_user_id, date_from=parsed_from, date_to=parsed_to)

    @http_get("/summary", auth=None)
    def summary(self, request, date_from: str | None = None, date_to: str | None = None):
        doctor_user_id = session_doctor_scope(request)
        parsed_from = date.fromisoformat(date_from) if date_from else None
        parsed_to = date.fromisoformat(date_to) if date_to else None
        return self.service.get_doctor_summary(doctor_user_id=doctor_user_id, date_from=parsed_from, date_to=parsed_to)
