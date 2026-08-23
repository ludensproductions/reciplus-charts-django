from ninja.schema import Schema

from apps.comun.consts import (
    ERROR_CREATE,
    ERROR_DELETE,
    ERROR_UPDATE,
    SUCCESS_CREATED,
    SUCCESS_DELETED,
    SUCCESS_UPDATED,
)


class MessageResponse(Schema):  # noqa
    message: str


class SuccessCreatedResponse(Schema):  # noqa
    message: str = SUCCESS_CREATED


class SuccessUpdatedResponse(Schema):  # noqa
    message: str = SUCCESS_UPDATED


class SuccessDeletedResponse(Schema):  # noqa
    message: str = SUCCESS_DELETED


class WrongCreateResponse(Schema):  # noqa
    message: str = ERROR_CREATE


class WrongUpdateResponse(Schema):  # noqa
    message: str = ERROR_UPDATE


class WrongDeleteResponse(Schema):  # noqa
    message: str = ERROR_DELETE
