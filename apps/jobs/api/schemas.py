from typing import List

from ninja import ModelSchema
from pydantic import ConfigDict, ValidationInfo, field_validator

from apps.comun.specifications.base import Specification
from apps.jobs.models import Job
from apps.jobs.specifications import (
    ValidRemoteLocationSpecification,
    ValidSalaryRangeSpecification,
)


def validate_with_spec(
    specs: List[Specification],
    value,
    info: ValidationInfo,
):
    """Validate a field value against a set of specifications.

    Args:
        specs (List[Specification]): Specifications to validate against.
        value: Field value being validated.
        info (ValidationInfo): Pydantic validation context.

    Returns:
        Any: The validated value.

    Raises:
        ValueError: When a specification is not satisfied.
    """
    # Build a lightweight object with current schema data + this field.
    job_data = dict(info.data)
    job_data[info.field_name] = value
    job = type("TempJob", (object,), job_data)()

    # Run through all given specifications.
    for spec in specs:
        if not spec.is_satisfied_by(job):
            # Prefer specification's message if available
            msg = getattr(spec, "message", f"Validation failed for {spec.__class__.__name__}.")
            raise ValueError(msg)

    return value


class JobSchemaIn(ModelSchema):  # noqa
    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "is_active",
            "is_remote",
            "location",
            "job_type",
            "max_salary",
            "min_salary",
        ]

    model_config = ConfigDict(extra="forbid")

    @field_validator("job_type", mode="before", check_fields=False)
    @classmethod
    def convert_enum_to_value(cls, v):  # noqa
        # If it's an Enum (like JobTypes.FULL_TIME), use its value
        return v.value if hasattr(v, "value") else v

    @field_validator("min_salary", check_fields=False)
    @classmethod
    def validate_min_salary(cls, value, info: ValidationInfo):  # noqa
        return validate_with_spec(
            [ValidSalaryRangeSpecification()],
            value,
            info,
        )

    @field_validator("location", check_fields=False)
    @classmethod
    def validate_location(cls, value, info: ValidationInfo):  # noqa
        return validate_with_spec(
            [ValidRemoteLocationSpecification()],
            value,
            info,
        )


class JobSchemaOut(ModelSchema):  # noqa
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
