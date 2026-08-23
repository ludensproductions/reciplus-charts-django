from enum import Enum
import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_generos import FieldGenerosEnum, PageGeneros

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


class ErrorMessages(Enum):
    """Mensajes de error esperados en el módulo de Géneros."""

    SPECIAL_CHARACTERS = "Este campo solo puede contener letras y espacios."

@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="GEN_01 Crear, validar y eliminar Género",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_genero(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.create_record(validate_record=True)
    await genero_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="GEN_02 Editar y validar Género",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_genero(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.create_record()
    await genero_page.edit_record(validate_record=True)
    await genero_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldGenerosEnum.DISPLAY_NAME.value,
            None,
            id="GEN_03 No crear con caracteres máximos en display_name",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldGenerosEnum.DISPLAY_NAME.value,
            None,
            id="GEN_04 No crear con display_name vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.NO_SPECIAL_CHARS,
            FieldGenerosEnum.DISPLAY_NAME.value,
            ErrorMessages.SPECIAL_CHARACTERS.value,
            id="GEN_07 No crear con display_name con caracteres especiales",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_genero_data(login_page, user, password, validate_type, field,custom_error_message):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_create_invalid_data(field, validate_type, custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldGenerosEnum.DISPLAY_NAME.value,
            None,
            id="GEN_05 No editar con caracteres máximos en display_name",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldGenerosEnum.DISPLAY_NAME.value,
            None,
            id="GEN_06 No editar con display_name vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.NO_SPECIAL_CHARS,
            FieldGenerosEnum.DISPLAY_NAME.value,
            ErrorMessages.SPECIAL_CHARACTERS.value,
            id="GEN_14 No editar con display_name con caracteres especiales",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_genero_data(login_page, user, password, validate_type, field, custom_error_message):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_edit_invalid_data(field, validate_type, custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldGenerosEnum.DISPLAY_NAME.value,
            id="GEN_08 Crear con solo letras en display_name",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_genero_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_09 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldGenerosEnum.DISPLAY_NAME.value,
            id="GEN_10 Filtrar por display_name",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.create_record()
    await genero_page.filter_by_specific_field(field)
    await genero_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_11 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_12 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_13 Habilitar género"),
    ],
)
@pytest.mark.asyncio
async def test_enable_genero(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldGenerosEnum.DISPLAY_NAME.value,
            id="GEN_15 Editar con solo letras en display_name",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_genero_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_16 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_17 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_18 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_19 Botón volver en detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_detail(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_back_button_on_detail()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_20 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_21 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_22 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_23 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GEN_24 Smoke CRUD género"),
    ],
)
@pytest.mark.asyncio
async def test_smoke_genero(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGeneros(page)
    await genero_page.create_record()
    await genero_page.validate_record()
    await genero_page.edit_record()
    await genero_page.validate_record()
    await genero_page.delete_record()
