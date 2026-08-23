from ninja import ModelSchema
from pydantic import ConfigDict

from ..models import Student


class StudentSchemaIn(ModelSchema):
    """Input schema for Student API operations used for create/update."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address"]


class StudentSchemaOut(ModelSchema):
    """Output schema for Student list and retrieve operations."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address"]


class CreateSchemaOut(ModelSchema):
    """Response schema for Student create operations."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address"]


class UpdateSchemaOut(ModelSchema):
    """Response schema for Student full update operations."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address"]


class PatchSchemaOut(ModelSchema):
    """Response schema for Student partial update operations."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address"]


class DeleteSchemaOut(ModelSchema):
    """Response schema for Student delete operations."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["name", "last_name", "email", "phone", "address"]


class StudentSchemaOutExtraFields(ModelSchema):
    """Schema with additional metadata fields for Student."""

    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Student
        fields = ["created_at", "updated_at", "deleted", "id"]
