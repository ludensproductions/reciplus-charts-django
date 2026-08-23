import pytest
from tests.pages.core.constants import InvalidDataType
from pages.catalogos.page_trabajos import INVALID_REMOTE_LOCATION_ERROR, FieldTrabajoEnum, PageTrabajos

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TRB_01 Crear, validar y eliminar Trabajo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_trabajo(login_page, user, password):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.create_record(validate_record=True)
    await trabajo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TRB_02 Editar y validar Trabajo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_trabajo(login_page, user, password):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.create_record()
    await trabajo_page.edit_record(validate_record=True)
    await trabajo_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTrabajoEnum.TITLE.value,
            id="TRB_03 No crear con caracteres máximos en título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTrabajoEnum.TITLE.value,
            id="TRB_04 No crear con título vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTrabajoEnum.COMPANY.value,
            id="TRB_05 No crear con caracteres máximos en compañía",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTrabajoEnum.COMPANY.value,
            id="TRB_06 No crear con compañía vacía",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTrabajoEnum.LOCATION.value,
            id="TRB_07 No crear con caracteres máximos en ubicación",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTrabajoEnum.LOCATION.value,
            id="TRB_08 No crear con ubicación vacía",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTrabajoEnum.JOB_TYPE.value,
            id="TRB_09 No crear con tipo de trabajo vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_trabajo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTrabajoEnum.TITLE.value,
            id="TRB_12 No editar con caracteres máximos en título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTrabajoEnum.TITLE.value,
            id="TRB_13 No editar con título vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_trabajo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TRB_16 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldTrabajoEnum.TITLE.value,
            id="TRB_17 Filtrar por título",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.create_record()
    await trabajo_page.filter_by_specific_field(field)
    await trabajo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TRB_18 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TRB_19 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TRB_23 Crear trabajo remoto con ubicación Remoto",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_remote_trabajo(login_page, user, password):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.create_record(validate_record=True, is_remote=True)
    await trabajo_page.delete_record()


@pytest.mark.parametrize(
    "user, password, field, custom_value, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldTrabajoEnum.LOCATION.value,
            True,
            INVALID_REMOTE_LOCATION_ERROR,
            id="TRB_24 No crear trabajo remoto con ubicación inválida",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_remote_location(login_page, user, password, field, custom_value, custom_error_message):
    page = await login_page(user, password)
    trabajo_page = PageTrabajos(page)
    await trabajo_page.validate_create_invalid_data(field_name=field, validate_type=InvalidDataType.CUSTOM, custom_error_message=custom_error_message, custom_value=custom_value, is_remote=True)
