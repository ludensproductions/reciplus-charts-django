from apps.comun.filters import AbstractFilter

from .const import VEHICLE_FILTER_FIELDS
from .models import Vehicle


class VehicleFilter(AbstractFilter):
    """Filter that exposes vehicle fields with translated labels."""

    class Meta:
        model = Vehicle
        fields = list(VEHICLE_FILTER_FIELDS.keys())
        fields_dict = VEHICLE_FILTER_FIELDS
