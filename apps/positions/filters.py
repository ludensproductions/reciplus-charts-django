from django.utils.translation import gettext_lazy as _

from apps.comun.filters import AbstractFilter

from .models import PuestoDepartamento

puesto_fields = {
    "departamento": {"label": _("Nombre del departamento")},
    "puesto__puesto": {"label": _("Nombre del puesto")},
    "jefe_departamento": {"label": _("Jefe de departamento")},
}


class PuestoFilter(AbstractFilter):
    # puesto_departamento__departamento =
    class Meta:
        model = PuestoDepartamento
        fields = list(puesto_fields.keys())
        fields_dict = puesto_fields
