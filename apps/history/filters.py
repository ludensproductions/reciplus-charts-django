import django_filters
from django.db import models
from django.utils.translation import gettext as _

from apps.users.models import User

LABELS_DICT = {
    "created_by": _("Creado por"),
    "created_at": _("Fecha de creación"),
    "updated_by": _("Actualizado por"),
    "updated_at": _("Fecha de actualización"),
    "deleted": _("Fecha de eliminación"),
    "history_date": _("Fecha cambio"),
    "history_type": _("Tipo de cambio"),
    "history_user": _("Usuario"),
    "display_name": _("Nombre de visualización"),
}

QUANTITY_TO_DELETE = 1000


class GenericFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)
        self.Meta.model = model

    class Meta:
        model = None  # Será reemplazado dinámicamente
        fields = "__all__"
        exclude = ["updated_by", "created_by"]


def create_dynamic_filter(model_class):
    class DynamicFilter(django_filters.FilterSet):
        def filter_user(queryset, name, value):
            return queryset.filter(**{f"{name}__username": value})

        def filter_avc(queryset, name, value):
            return queryset.filter(**{f"{name}__numero_avc": value})

        def filter_dates(queryset, name, value):
            year = value.year
            month = value.month
            day = value.day
            return queryset.filter(**{f"{name}__year": year, f"{name}__month": month, f"{name}__day": day})

        class Meta:
            model = model_class
            fields = "__all__"  # O especifica los campos que deseas incluir en el filtro
            exclude = [
                "deleted_by_cascade",
                "signature_date",
                "signature",
                "password",
                "history_change_reason",
            ]
            filter_overrides = {
                models.FileField: {
                    "filter_class": django_filters.CharFilter,
                    "extra": lambda f: {
                        "lookup_expr": "icontains",
                    },
                },
                models.JSONField: {
                    "filter_class": django_filters.CharFilter,
                    "extra": lambda f: {
                        "lookup_expr": "icontains",
                    },
                },
                # models.ManyToManyField: {
                #     'filter_class': django_filters.ModelMultipleChoiceFilter,
                # Cambia aquí a ModelMultipleChoiceFilter
                #     'extra': lambda f: {
                #         'to_field_name': f.related_model.name,  # Obtiene el nombre del campo relacionado
                #         'queryset': f.related_model.objects.all(),
                #     },
                # },
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name in self.get_fields():
                if field_name in LABELS_DICT:
                    self.filters[field_name].label = LABELS_DICT[field_name]
                    self.filters[field_name].field.widget.attrs.update({"placeholder": LABELS_DICT[field_name]})

                if self._meta.model._meta.get_field(field_name).related_model:
                    if self._meta.model._meta.get_field(field_name).related_model == User:
                        self.filters[field_name] = django_filters.CharFilter(
                            label=LABELS_DICT[field_name] if field_name in LABELS_DICT else field_name.title(),
                            lookup_expr="icontains",
                            method=DynamicFilter.filter_user,
                            field_name=field_name,
                        )
                    else:
                        model = self._meta.model._meta.get_field(field_name).related_model
                        records = model.objects.all()
                        if records.count() > QUANTITY_TO_DELETE:
                            del self.filters[field_name]
                            continue
                if self._meta.model._meta.get_field(field_name).__class__.__name__ == "JSONField":
                    del self.filters[field_name]
                    continue

                if self._meta.model._meta.get_field(field_name).__class__.__name__ == "ManyToManyField":
                    del self.filters[field_name]
                    continue

                label_name = field_name.replace("_", " ").capitalize()

                self.filters[field_name].field.widget.attrs.update(
                    {
                        "class": "form-control",
                        "placeholder": LABELS_DICT[field_name] if field_name in LABELS_DICT else label_name,
                    }
                )
                if self.filters[field_name].__class__.__name__ == "CharFilter":
                    self.filters[field_name].lookup_expr = "icontains"

                elif (
                    self.filters[field_name].__class__.__name__ == "DateFilter"
                    or self.filters[field_name].__class__.__name__ == "DateTimeFilter"
                ):
                    self.filters[field_name].field.widget.input_type = "date"
                    self.filters[field_name].method = DynamicFilter.filter_dates

    return DynamicFilter
