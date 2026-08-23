from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.consts import CRUDOperatorsEnum
from apps.comun.models import AbstractModel
from apps.students.consts import (
    COURSE_LABEL,
    STUDENT_ADDRESS_LABEL,
    STUDENT_COURSE_MODEL_VERBOSE_NAME,
    STUDENT_COURSE_MODEL_VERBOSE_NAME_PLURAL,
    STUDENT_COURSES_LABEL,
    STUDENT_EMAIL_LABEL,
    STUDENT_GRADE_LABEL,
    STUDENT_IMAGE_LABEL,
    STUDENT_LAST_NAME_LABEL,
    STUDENT_MODEL_VERBOSE_NAME,
    STUDENT_MODEL_VERBOSE_NAME_PLURAL,
    STUDENT_NAME_LABEL,
    STUDENT_PHONE_LABEL,
)


class Student(AbstractModel):
    """Represents a student profile within the academic catalog.

    This entity stores identity and contact attributes for students and
    links them to courses through the StudentCourse relation.

    Side Effects:
        Persists student records and relation metadata used by CRUD and API
        generators.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(STUDENT_NAME_LABEL, max_length=255)
    last_name = models.CharField(STUDENT_LAST_NAME_LABEL, max_length=255)
    email = models.EmailField(STUDENT_EMAIL_LABEL, max_length=255)
    phone = models.CharField(STUDENT_PHONE_LABEL, max_length=255)
    address = models.CharField(STUDENT_ADDRESS_LABEL, max_length=255)
    image = models.ImageField(
        STUDENT_IMAGE_LABEL,
        upload_to="profiles/",
        max_length=255,
        blank=True,
        null=True,
        default="/static/assets/img/avatars/blank-profile-pic.png",
    )
    courses = models.ManyToManyField(
        "courses.Course",
        through="students.StudentCourse",
        related_name="students",
        verbose_name=STUDENT_COURSES_LABEL,
    )

    class Meta:
        """Django model metadata for storage and admin presentation."""

        db_table = "students"
        verbose_name = STUDENT_MODEL_VERBOSE_NAME
        verbose_name_plural = STUDENT_MODEL_VERBOSE_NAME_PLURAL
        ordering = ["id"]

    class Config:
        """Configuration used by internal CRUD/API autogeneration.

        Attributes:
            crud_operations (list[CRUDOperatorsEnum]): CRUD operations to scaffold.
                Presence of this list enables CRUD generation.
            api_operations (list[CRUDOperatorsEnum]): API operations to scaffold.
                Presence of this list enables API generation.
        """

        crud_operations = [
            CRUDOperatorsEnum.INDEX,
            CRUDOperatorsEnum.CREATE,
            CRUDOperatorsEnum.READ,
            CRUDOperatorsEnum.UPDATE,
            CRUDOperatorsEnum.DELETE,
        ]
        api_operations = [
            CRUDOperatorsEnum.INDEX,
            CRUDOperatorsEnum.CREATE,
            CRUDOperatorsEnum.READ,
            CRUDOperatorsEnum.UPDATE,
            CRUDOperatorsEnum.DELETE,
        ]

    def __str__(self):
        """Return the full name for display.

        Returns:
            str: Student full name.
        """
        return f"{self.name} {self.last_name}"


class StudentCourse(AbstractModel):
    """Associates students with courses and stores an optional grade.

    This join entity represents enrollment records and supports grade
    registration per student-course relationship.

    Side Effects:
        Persists enrollment rows that define many-to-many relationships
        between students and courses.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="student_courses",
        verbose_name=STUDENT_MODEL_VERBOSE_NAME,
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="student_courses",
        verbose_name=COURSE_LABEL,
    )
    grade = models.DecimalField(STUDENT_GRADE_LABEL, max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        """Django model metadata for enrollment storage and labels."""

        db_table = "students_courses"
        verbose_name = STUDENT_COURSE_MODEL_VERBOSE_NAME
        verbose_name_plural = STUDENT_COURSE_MODEL_VERBOSE_NAME_PLURAL
        ordering = ["id"]

    def __str__(self):
        """Return the record identifier.

        Returns:
            str: StudentCourse identifier.
        """
        return str(self.id)
