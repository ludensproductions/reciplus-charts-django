from datetime import date, timedelta

from django.db.models import F, Q

from apps.comun.specifications.base import Specification
from apps.jobs.consts import (
    ACTIVE_JOB_COMPANY_RESTRICTION_VALUE,
    COMPANY_BLACKLIST,
    ERROR_COMPANY_INACTIVE_RESTRICTION,
    ERROR_COMPANY_NOT_ALLOWED,
    ERROR_REMOTE_LOCATION_INVALID,
    ERROR_SALARY_RANGE_INVALID,
    ERROR_TITLE_INVALID,
    VALID_REMOTE_LOCATION_VALUES,
)


class ActiveJobSpecification(Specification):
    """Specification that matches active jobs."""

    def is_satisfied_by(self, job):
        """Check whether the job is active.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the job is active.
        """
        return job.is_active

    def as_q(self):
        """Return a queryset filter for active jobs.

        Returns:
            Q: Query expression for active jobs.
        """
        return Q(is_active=True)


class RemoteJobSpecification(Specification):
    """Specification that matches remote jobs."""

    def is_satisfied_by(self, job):
        """Check whether the job is remote.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the job is remote.
        """
        return job.is_remote

    def as_q(self):
        """Return a queryset filter for remote jobs.

        Returns:
            Q: Query expression for remote jobs.
        """
        return Q(is_remote=True)


class LocationSpecification(Specification):
    """Specification that matches jobs by location."""

    def __init__(self, location):
        self.location = location

    def is_satisfied_by(self, job):
        """Check whether the job location matches the filter.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the location matches.
        """
        return job.location.lower() == self.location.lower()

    def as_q(self):
        """Return a queryset filter for the location.

        Returns:
            Q: Query expression for location.
        """
        return Q(location__iexact=self.location)


class SalaryAboveSpecification(Specification):
    """Specification that matches jobs above a salary threshold."""

    def __init__(self, min_salary):
        self.min_salary = min_salary

    def is_satisfied_by(self, job):
        """Check whether the job meets the salary threshold.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the minimum salary is sufficient.
        """
        return job.min_salary >= self.min_salary

    def as_q(self):
        """Return a queryset filter for minimum salary.

        Returns:
            Q: Query expression for minimum salary.
        """
        return Q(min_salary__gte=self.min_salary)


class RecentlyPostedSpecification(Specification):
    """Specification that matches recently posted jobs."""

    def __init__(self, days=7):
        self.days = days

    def is_satisfied_by(self, job):
        """Check whether the job was created within the allowed window.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the job is recent.
        """
        return (date.today() - job.created_at).days <= self.days

    def as_q(self):
        """Return a queryset filter for recently created jobs.

        Returns:
            Q: Query expression for recent jobs.
        """
        cutoff = date.today() - timedelta(days=self.days)
        return Q(created_at__gte=cutoff)


class ValidSalaryRangeSpecification(Specification):
    """Validate that min_salary is not greater than max_salary."""

    message = ERROR_SALARY_RANGE_INVALID

    def is_satisfied_by(self, job):
        """Check whether the salary range is valid.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the salary range is valid.
        """
        return job.min_salary <= job.max_salary

    def as_q(self):
        """Return a queryset filter for valid salary ranges.

        Returns:
            Q: Query expression for valid salary ranges.
        """
        return Q(min_salary__lte=F("max_salary"))


class ValidRemoteLocationSpecification(Specification):
    """Validate location for remote jobs."""

    message = ERROR_REMOTE_LOCATION_INVALID

    def is_satisfied_by(self, job):
        """Check whether the remote location value is valid.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the location is valid for the remote flag.
        """
        if not job.is_remote:
            return True
        return job.location.lower() in VALID_REMOTE_LOCATION_VALUES

    def as_q(self):
        """Return an empty query expression.

        Returns:
            Q: Empty query expression.
        """
        return Q()


class ActiveJobCompanyRestrictionSpecification(Specification):
    """Validate active status for restricted companies."""

    message = ERROR_COMPANY_INACTIVE_RESTRICTION

    def is_satisfied_by(self, job):
        """Check whether the job satisfies the active restriction.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the restriction is satisfied.
        """
        if job.company.lower() == ACTIVE_JOB_COMPANY_RESTRICTION_VALUE.lower() and not job.is_active:
            return False
        return True

    def as_q(self):
        """Return an empty query expression.

        Returns:
            Q: Empty query expression.
        """
        return Q()


class ValidTitleSpecification(Specification):
    """Validate job titles for minimum length and spacing."""

    message = ERROR_TITLE_INVALID

    def is_satisfied_by(self, job) -> bool:
        """Check whether the title meets the requirements.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the title is valid.
        """
        return len(job.title.strip()) >= 5 and " " in job.title

    def as_q(self):
        """Return an empty query expression.

        Returns:
            Q: Empty query expression.
        """
        return Q()


class CompanyBlacklistSpecification(Specification):
    """Validate that the company is not blacklisted."""

    message = ERROR_COMPANY_NOT_ALLOWED

    def is_satisfied_by(self, job) -> bool:
        """Check whether the company is allowed.

        Args:
            job: Job instance to validate.

        Returns:
            bool: True when the company is not blacklisted.
        """
        return job.company not in COMPANY_BLACKLIST

    def as_q(self):
        """Return an empty query expression.

        Returns:
            Q: Empty query expression.
        """
        return Q()
