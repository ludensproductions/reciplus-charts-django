from django import forms
from django.forms.widgets import DateInput, DateTimeInput

from apps.comun.forms import (
    AbstractModelForm,
)
from apps.comun.widgets import RangeWidget

from .consts import (
    CARGO_EXTRA,
    ERROR_CANCEL_START_AFTER_END,
    FECHA_FIN_CANCELACION,
    FECHA_HORA_LLEGADA,
    FECHA_INICIO_CANCELACION,
    FECHAS_RESERVACION,
    PLACEHOLDER_NOMBRE_RESERVADOR,
    PUNTOS_PROMOCION,
    RESERVADOR,
    TIEMPO_LIMITE_CANCELACION,
    TIPO_RESERVACION,
)
from .models import Reservation


# crear formulario
class ReservationForm(AbstractModelForm):
    """Form for creating and updating Reservation instances.

    Handles validation for reservation booking ranges, cancellation periods,
    and ensures that cancellation dates are logically consistent.
    """

    class Meta:
        model = Reservation
        fields = [
            "guest",
            "booking_range",
            "cancel_start",
            "cancel_end",
            "cancel_time",
            "scheduled_arrive",
            "reservation_type",
            "extra_fee",
            "promotion_points",
        ]  # You can change this for the field"s name
        exclude = ["deleted", "deleted_at", "created_by", "updated_by"]

        labels = {
            "guest": RESERVADOR,
            "booking_range": FECHAS_RESERVACION,
            "cancel_start": FECHA_INICIO_CANCELACION,
            "cancel_end": FECHA_FIN_CANCELACION,
            "scheduled_arrive": FECHA_HORA_LLEGADA,
            "reservation_type": TIPO_RESERVACION,
            "extra_fee": CARGO_EXTRA,
            "promotion_points": PUNTOS_PROMOCION,
            "cancel_time": TIEMPO_LIMITE_CANCELACION,
        }

        widgets = {
            "guest": forms.TextInput(attrs={"placeholder": PLACEHOLDER_NOMBRE_RESERVADOR}),
            "booking_range": RangeWidget(
                base_widget=DateInput({"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
            ),
            "cancel_start": DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
            "cancel_end": DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
            "cancel_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}, format="%H:%M"),
            "scheduled_arrive": DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def clean(self):
        """Validate that cancellation period dates are consistent.

        Adds an error to the cancel_start field if it is after cancel_end.

        Returns:
            dict: The cleaned data dictionary.
        """
        cleaned_data = super().clean()
        cancel_start = cleaned_data.get("cancel_start")
        cancel_end = cleaned_data.get("cancel_end")

        if cancel_start and cancel_end:
            if cancel_start > cancel_end:
                self.add_error("cancel_start", ERROR_CANCEL_START_AFTER_END)

        return cleaned_data
