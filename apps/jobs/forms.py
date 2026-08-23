from django import forms

from apps.comun.forms import AbstractModelForm

from .consts import (
    ERROR_COMPANY_INACTIVE_RESTRICTION,
    ERROR_COMPANY_NOT_ALLOWED,
    ERROR_REMOTE_LOCATION_INVALID,
    ERROR_SALARY_RANGE_INVALID,
    ERROR_TITLE_INVALID,
    FORM_COMPANY_LABEL,
    FORM_COMPANY_PLACEHOLDER,
    FORM_IS_ACTIVE_LABEL,
    FORM_IS_REMOTE_LABEL,
    FORM_JOB_TYPE_LABEL,
    FORM_JOB_TYPE_PLACEHOLDER,
    FORM_LOCATION_LABEL,
    FORM_LOCATION_PLACEHOLDER,
    FORM_MAX_SALARY_LABEL,
    FORM_MAX_SALARY_PLACEHOLDER,
    FORM_MIN_SALARY_LABEL,
    FORM_MIN_SALARY_PLACEHOLDER,
    FORM_TITLE_LABEL,
    FORM_TITLE_PLACEHOLDER,
)
from .models import Job
from .specifications import (
    ActiveJobCompanyRestrictionSpecification,
    CompanyBlacklistSpecification,
    ValidRemoteLocationSpecification,
    ValidSalaryRangeSpecification,
    ValidTitleSpecification,
)


class JobForm(AbstractModelForm):
    """Form for creating and updating job records."""

    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "location",
            "job_type",
            "min_salary",
            "max_salary",
            "is_remote",
            "is_active",
        ]

        labels = {
            "title": FORM_TITLE_LABEL,
            "company": FORM_COMPANY_LABEL,
            "location": FORM_LOCATION_LABEL,
            "job_type": FORM_JOB_TYPE_LABEL,
            "min_salary": FORM_MIN_SALARY_LABEL,
            "max_salary": FORM_MAX_SALARY_LABEL,
            "is_remote": FORM_IS_REMOTE_LABEL,
            "is_active": FORM_IS_ACTIVE_LABEL,
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": FORM_TITLE_PLACEHOLDER}),
            "company": forms.TextInput(attrs={"placeholder": FORM_COMPANY_PLACEHOLDER}),
            "location": forms.TextInput(attrs={"placeholder": FORM_LOCATION_PLACEHOLDER}),
            "job_type": forms.Select(attrs={"placeholder": FORM_JOB_TYPE_PLACEHOLDER}),
            "min_salary": forms.NumberInput(attrs={"placeholder": FORM_MIN_SALARY_PLACEHOLDER}),
            "max_salary": forms.NumberInput(attrs={"placeholder": FORM_MAX_SALARY_PLACEHOLDER}),
            "is_remote": forms.CheckboxInput(attrs={"placeholder": FORM_IS_REMOTE_LABEL}),
            "is_active": forms.CheckboxInput(attrs={"placeholder": FORM_IS_ACTIVE_LABEL}),
        }

    def clean(self):
        """Validate combined business rules for job data.

        Returns:
            dict: Cleaned form data.
        """
        cleaned_data = super().clean()
        job = Job(**cleaned_data)

        # Define reusable combined specifications.
        general_spec = (
            ValidSalaryRangeSpecification()
            & ValidRemoteLocationSpecification()
            & ActiveJobCompanyRestrictionSpecification()
        )

        # Validate combined rule.
        if not general_spec.is_satisfied_by(job):
            # You can still introspect which individual specs failed.
            failed_specs = [
                spec.__class__.__name__ for spec in general_spec.flatten() if not spec.is_satisfied_by(job)
            ]

            messages = {
                "ValidSalaryRangeSpecification": {
                    "field_name": "min_salary",
                    "error": forms.ValidationError(ERROR_SALARY_RANGE_INVALID),
                },
                "ValidRemoteLocationSpecification": {
                    "field_name": "location",
                    "error": forms.ValidationError(ERROR_REMOTE_LOCATION_INVALID),
                },
                "ActiveJobCompanyRestrictionSpecification": {
                    "field_name": "is_active",
                    "error": forms.ValidationError(ERROR_COMPANY_INACTIVE_RESTRICTION),
                },
            }

            for name in failed_specs:
                message = messages.get(name)
                self.add_error(
                    field=message.get("field_name"),
                    error=message.get("error"),
                )

        return cleaned_data

    def clean_title(self):
        """Validate the job title format.

        Returns:
            str: Validated title value.
        """
        title = self.cleaned_data.get("title")
        job = Job(**self.cleaned_data)
        spec = ValidTitleSpecification()
        if not spec.is_satisfied_by(job):
            raise forms.ValidationError(ERROR_TITLE_INVALID)
        return title

    def clean_company(self):
        """Validate the company against the blacklist.

        Returns:
            str: Validated company value.
        """
        company = self.cleaned_data.get("company")
        job = Job(**self.cleaned_data)
        spec = CompanyBlacklistSpecification()
        if not spec.is_satisfied_by(job):
            raise forms.ValidationError(ERROR_COMPANY_NOT_ALLOWED)
        return company
