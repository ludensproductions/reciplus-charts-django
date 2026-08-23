from apps.comun.filters import AbstractFilter

from .consts import (
    STUDENT_ADDRESS_FILTER_LABEL,
    STUDENT_EMAIL_FILTER_LABEL,
    STUDENT_LAST_NAME_FILTER_LABEL,
    STUDENT_NAME_FILTER_LABEL,
    STUDENT_PHONE_FILTER_LABEL,
)
from .models import Student

student_fields = {
    "name": {"label": STUDENT_NAME_FILTER_LABEL},
    "last_name": {"label": STUDENT_LAST_NAME_FILTER_LABEL},
    "email": {"label": STUDENT_EMAIL_FILTER_LABEL},
    "phone": {"label": STUDENT_PHONE_FILTER_LABEL},
    "address": {"label": STUDENT_ADDRESS_FILTER_LABEL},
}


class StudentFilter(AbstractFilter):
    """Filter configuration for student list views.

    This filter maps student model fields to user-facing labels used by the
    filtering UI in index screens.

    Attributes:
        Meta (type): Django filter metadata with model binding and allowed
            filter fields.
    """

    class Meta:
        model = Student
        fields = list(student_fields.keys())
        fields_dict = student_fields
