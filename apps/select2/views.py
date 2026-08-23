from django_select2.views import AutoResponseView


class CustomAutoResponseView(AutoResponseView):
    """Customize Select2 responses for dependent fields."""

    def get_queryset(self):
        """Get queryset from the cached widget.

        Returns:
            QuerySet: Filtered queryset based on widget dependencies.
        """
        require_dependencies = getattr(self.widget, "require_dependencies", False)

        kwargs = {
            model_field_name: self.request.GET.get(form_field_name)
            for form_field_name, model_field_name in self.widget.dependent_fields.items()
        }

        if require_dependencies and not any(kwargs.values()):
            return self.widget.queryset.none()

        kwargs.update(
            {
                f"{model_field_name}__in": self.request.GET.getlist(f"{form_field_name}[]", [])
                for form_field_name, model_field_name in self.widget.dependent_fields.items()
            }
        )
        return self.widget.filter_queryset(
            self.request,
            self.term,
            self.queryset,
            **{k: v for k, v in kwargs.items() if v},
        )
