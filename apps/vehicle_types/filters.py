from apps.comun.filters import AbstractFilter

from .consts import VEHICLE_TYPE_FILTER_FIELDS
from .models import VehicleType


class VehicleTypeFilter(AbstractFilter):
    """Provide filtering over vehicle types."""

    class Meta:
        model = VehicleType
        fields = list(VEHICLE_TYPE_FILTER_FIELDS.keys())
        fields_dict = VEHICLE_TYPE_FILTER_FIELDS
