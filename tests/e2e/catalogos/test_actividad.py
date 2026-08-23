import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_actividad import FieldActividadEnum, PageActividad

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="ACT_01 Crear, validar y eliminar Actividad",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_actividad(login_page, user, password):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.create_record(validate_record=True)
    await actividad_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="ACT_02 Editar y validar Actividad",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_actividad(login_page, user, password):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.create_record()
    await actividad_page.edit_record(validate_record=True)
    await actividad_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_03 No crear con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_04 No crear con nombre vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldActividadEnum.UBICACION.value,
            id="ACT_05 No crear con caracteres máximos en ubicación",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldActividadEnum.UBICACION.value,
            id="ACT_06 No crear con ubicación vacía",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_actividad_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_07 No editar con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_08 No editar con nombre vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldActividadEnum.UBICACION.value,
            id="ACT_09 No editar con caracteres máximos en ubicación",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldActividadEnum.UBICACION.value,
            id="ACT_10 No editar con ubicación vacía",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_actividad_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_11 Crear con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_12 Crear con solo letras en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldActividadEnum.UBICACION.value,
            id="ACT_13 Crear con caracteres especiales en ubicación",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldActividadEnum.UBICACION.value,
            id="ACT_14 Crear con solo letras en ubicación",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_actividad_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_15 Editar con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_16 Editar con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_actividad_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="ACT_17 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldActividadEnum.NOMBRE.value,
            id="ACT_18 Filtrar por nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.create_record()
    await actividad_page.filter_by_specific_field(field)
    await actividad_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="ACT_19 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="ACT_20 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    actividad_page = PageActividad(page)
    await actividad_page.validate_clear_filters_button()
