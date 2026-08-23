from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE

from apps.comun.models import AbstractNullableModel
from apps.departments import consts as departments_consts


class Departamento(AbstractNullableModel):
    """Represent a department within the organization.

    This model stores department names and optional parent departments for
    hierarchical relationships. Related positions and group assignments are
    configured for cascade deletion.

    Attributes:
        nombre_departamento (str): Department name.
        departamento_superior (Departamento | None): Parent department.
    """

    _safe_delete_policy = SOFT_DELETE
    nombre_departamento = models.CharField(max_length=255, verbose_name=departments_consts.DEPARTMENT_NAME_LABEL)
    departamento_superior = models.ForeignKey(
        "Departamento",
        related_name="departamento_inferior",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name=departments_consts.PARENT_DEPARTMENT_LABEL,
    )

    # Cascade delete related positions and group assignments when deleting a department.
    delete_on_cascade = [
        "puestos_departamento",
        "grupos_departamentos",
        "puestos_departamento__puesto_departamento_groups",
    ]
    # child_relations = [
    #     ("PuestoDepartamento", "puestos_departamento", "positions:index"),
    #     ("GruposDepartamento", "grupos_departamentos", "departments:index")
    # ]

    class Meta:
        verbose_name = departments_consts.INDEX_FIELDS["nombre_departamento"]
        verbose_name_plural = departments_consts.INDEX_TITLE
        db_table = "departamento"
        ordering = ["-id"]

        permissions = (("enable_departamento", _("Puede habilitar departamento")),)

    def __str__(self):
        """Return the department name.

        Returns:
            str: Department name.
        """
        return self.nombre_departamento


class GruposDepartamento(AbstractNullableModel):
    """Link a department with a custom group."""

    _safe_delete_policy = SOFT_DELETE
    auth_group = models.ForeignKey(
        "groups.CustomGroup",
        related_name="dept_groups",
        related_query_name="departamento_groups",
        on_delete=models.DO_NOTHING,
        verbose_name=departments_consts.GROUPS_LABEL,
    )
    departamento = models.ForeignKey(
        "Departamento",
        related_name="grupos_departamentos",
        on_delete=models.DO_NOTHING,
        verbose_name=departments_consts.INDEX_FIELDS["nombre_departamento"],
    )

    class Meta:
        verbose_name = _("Grupo de departamento")
        verbose_name_plural = _("Grupos de departamento")
        db_table = "dept_groups"
        ordering = ["-id"]
