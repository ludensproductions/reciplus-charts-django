from django.db import models

from apps.comun.models import AbstractModel
from apps.jobs.consts import (
    FIELD_COMPANY_LABEL,
    FIELD_IS_ACTIVE_LABEL,
    FIELD_IS_REMOTE_LABEL,
    FIELD_JOB_TYPE_LABEL,
    FIELD_LOCATION_LABEL,
    FIELD_MAX_SALARY_LABEL,
    FIELD_MIN_SALARY_LABEL,
    FIELD_TITLE_LABEL,
    MODEL_JOB_VERBOSE_NAME,
    MODEL_JOB_VERBOSE_NAME_PLURAL,
    JobTypes,
)


class Job(AbstractModel):
    """Represent a job posting with salary and location details.

    This model stores the core metadata used to publish and filter jobs.
    """

    title = models.CharField(max_length=200, verbose_name=FIELD_TITLE_LABEL)
    company = models.CharField(max_length=100, verbose_name=FIELD_COMPANY_LABEL)
    location = models.CharField(max_length=100, verbose_name=FIELD_LOCATION_LABEL)
    job_type = models.CharField(max_length=20, choices=JobTypes, verbose_name=FIELD_JOB_TYPE_LABEL)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=FIELD_MIN_SALARY_LABEL)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=FIELD_MAX_SALARY_LABEL)
    is_remote = models.BooleanField(default=False, verbose_name=FIELD_IS_REMOTE_LABEL)
    is_active = models.BooleanField(default=True, verbose_name=FIELD_IS_ACTIVE_LABEL)

    class Meta:
        db_table = "job"
        verbose_name = MODEL_JOB_VERBOSE_NAME
        verbose_name_plural = MODEL_JOB_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return a display string for the job.

        Returns:
            str: Job title and company name.
        """
        return f"{self.title} - {self.company}"
