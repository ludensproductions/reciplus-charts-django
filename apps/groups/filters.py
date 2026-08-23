from django.utils.translation import gettext_lazy as _

from apps.comun.filters import AbstractFilter

from .models import CustomGroup

group_fields = {
    "display_name": {"label": _("Grupo")},
}


class GroupFilter(AbstractFilter):
    class Meta:
        model = CustomGroup
        fields = list(group_fields.keys())
        fields_dict = group_fields
