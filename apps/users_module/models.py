from django.db import models

from .consts import MODEL_VERBOSE_NAME, MODEL_VERBOSE_NAME_PLURAL, PERMISSION_VIEW


class UsersModule(models.Model):
    """Proxy model to manage user module permissions.

    This model serves as a container for custom permissions related to the
    users module functionality. It provides a mechanism to organize and control
    access to user management operations.
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("view_users_module", PERMISSION_VIEW),)
        verbose_name = MODEL_VERBOSE_NAME
        verbose_name_plural = MODEL_VERBOSE_NAME_PLURAL
