from django.utils.translation import gettext_lazy as _

from apps.comun.filters import AbstractFilter

from .models import VehicleBrand

# Diccionario de campos a mostrar en el filtro
vehicle_brand_fields = {
    "name": {"label": _("Marca")},
}


class VehicleBrandFilter(AbstractFilter):
    """Filter configuration for vehicle brand listing views."""

    class Meta:
        """Bind filter fields to the VehicleBrand model."""

        model = VehicleBrand
        fields = list(vehicle_brand_fields.keys())
        fields_dict = vehicle_brand_fields
