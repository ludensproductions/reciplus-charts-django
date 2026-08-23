# Create your models here.
from django.db import models
from simple_history.models import HistoricalRecords

from .abstract_methods import AbstractMethodsMixin


# Create your models here.
class AbstractModel(AbstractMethodsMixin):
    """Abstract base model with audit fields and history.

    This model provides created/updated timestamps, user references, and
    historical tracking for concrete models that require full audit data.

    Attributes:
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
        created_by: User who created the record.
        updated_by: User who last updated the record (optional).
        history: Simple history manager for audit tracking.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey("users.User", related_name="+", on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey("users.User", related_name="+", on_delete=models.DO_NOTHING, null=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class AbstractNullableModel(AbstractMethodsMixin):
    """Abstract base model with nullable audit fields and history.

    This model is intended for cases where creator/updater are optional but
    audit timestamps and history are still required.

    Attributes:
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
        created_by: User who created the record (optional).
        updated_by: User who last updated the record (optional).
        history: Simple history manager for audit tracking.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey("users.User", related_name="+", on_delete=models.DO_NOTHING, null=True)
    updated_by = models.ForeignKey("users.User", related_name="+", on_delete=models.DO_NOTHING, null=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


# Do not use this model, ask before using it, this model is for models that do not need created_by and updated_by fields, but we want to keep the created_at and updated_at fields, as well as the history.
class AbstrasModelNoUser(AbstractMethodsMixin):
    """Abstract base model without user references.

    This model keeps only timestamps and history for records that do not
    track creator/updater users.

    Attributes:
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
        history: Simple history manager for audit tracking.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
