from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE

from apps.comun.models import AbstractNullableModel
from apps.departments.models import Departamento
from apps.groups.models import CustomGroup


class Puesto(AbstractNullableModel):
    _safe_delete_policy = SOFT_DELETE
    puesto = models.CharField(max_length=255)

    # Al eliminar un Puesto queremos que se eliminen en cascada los PuestoDepartamento
    delete_on_cascade = ["puestos_departamentos"]
    # child_relations = [
    #     ("PuestoDepartamento", "puestos_departamentos", "positions:index")
    # ]

    class Meta:
        verbose_name = _("Puesto")
        verbose_name_plural = _("Puestos")
        db_table = "puesto"
        ordering = ["-id"]

    def __str__(self):
        return self.puesto if len(self.puesto) < 100 else self.puesto[:100] + "..."


class PuestoDepartamento(AbstractNullableModel):
    _safe_delete_policy = SOFT_DELETE
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING, related_name="puestos_departamento")
    puesto = models.ForeignKey(
        "Puesto",
        related_name="puestos_departamentos",
        related_query_name="puesto_departamento",
        on_delete=models.DO_NOTHING,
    )
    jefe_departamento = models.BooleanField(default=False, blank=True)

    # Al eliminar un PuestoDepartamento se eliminarán en cascada los PositionGroup asociados.
    delete_on_cascade = ["puesto_departamento_groups"]
    # child_relations = [
    #     ("PositionGroup", "puesto_departamento_groups", "positions:index")
    # ]

    class Meta:
        verbose_name = _("Puesto Departamento")
        verbose_name_plural = _("Puestos Departamentos")
        db_table = "puesto_departamento"
        ordering = ["-id"]

    @property
    def is_jefe_departamento(self):
        return _("Sí") if self.jefe_departamento else _("No")


class PositionGroup(AbstractNullableModel):
    _safe_delete_policy = SOFT_DELETE
    auth_group = models.ForeignKey(
        CustomGroup,
        related_name="group_puesto_departamentos",
        related_query_name="group_puesto_departamento",
        on_delete=models.DO_NOTHING,
    )
    puesto_departamento = models.ForeignKey(
        "PuestoDepartamento", related_name="puesto_departamento_groups", on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = _("Grupo de puesto")
        verbose_name_plural = _("Grupos de puesto")
        db_table = "position_groups"
        ordering = ["-id"]
