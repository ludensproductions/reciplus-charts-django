from django.db import models

from apps.catalogos import consts as catalogos_consts


class CatalogosModule(models.Model):
    """Expose the catalog module for permission checks.

    This unmanaged model exists to register the `view_catalogos` permission
    and group catalog-related access under a single content type.
    """

    class Meta:
        managed = False
        default_permissions = ()
        verbose_name = catalogos_consts.MODEL_VERBOSE_NAME
        verbose_name_plural = catalogos_consts.MODEL_VERBOSE_NAME_PLURAL
        permissions = (("view_catalogos", catalogos_consts.PERMISSION_VIEW_LABEL),)
