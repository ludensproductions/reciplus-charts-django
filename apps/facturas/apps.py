from django.apps import AppConfig


class FacturasConfig(AppConfig):
    """Configure the Facturas Django application.

    Attributes:
        default_auto_field (str): Default primary key field type for models.
        name (str): Django app label with full Python path.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.facturas"
