from http import HTTPStatus
from typing import List

from ninja_extra import http_get
from ninja_jwt.authentication import JWTAuth

from apps.comun.api.controller import BaseApiController
from apps.comun.api.decorator import api_controller
from apps.jobs.api.schemas import JobSchemaIn, JobSchemaOut
from apps.jobs.models import Job
from apps.jobs.specifications import (
    LocationSpecification,
    RemoteJobSpecification,
    SalaryAboveSpecification,
)


@api_controller("/jobs", tags=["Jobs"], auth=JWTAuth())
class JobController(BaseApiController):  # noqa
    model = Job

    create_schema = JobSchemaIn
    retrieve_schema = JobSchemaOut

    create_route_info = {"auth": None}

    @http_get(
        "/get-remote-jobs",
        auth=None,
        response={
            HTTPStatus.OK: List[JobSchemaOut],
        },
    )
    def get_only_remote(self, request):
        """Endpoint to only get remote jobs."""
        spec = RemoteJobSpecification()
        return self.model.objects.filter(spec.as_q())

    @http_get(
        "/get-jobs-above-specified",
        auth=None,
        response={
            HTTPStatus.OK: List[JobSchemaOut],
        },
    )
    def get_jobs_above_specified(self, request, min_salary: int):
        """Endpoint to only get jobs that have a salary above the specified amount."""
        spec = SalaryAboveSpecification(min_salary=min_salary)
        return self.model.objects.filter(spec.as_q())

    @http_get(
        "/get-by-location",
        auth=None,
        response={
            HTTPStatus.OK: List[JobSchemaOut],
        },
    )
    def get_by_location(self, request, location: str):
        """Endpoint to only get jobs that have a certain specified location."""
        spec = LocationSpecification(location=location)
        return self.model.objects.filter(spec.as_q())
