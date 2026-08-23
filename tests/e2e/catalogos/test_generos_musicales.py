import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_generos_musicales import FieldGenerosMusicalesEnum, PageGenerosMusicales

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TGM_01 Crear, validar y eliminar Género musical",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_genero_musical(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.create_record(validate_record=True)
    await genero_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TGM_02 Editar y validar Género musical",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_genero_musical(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.create_record()
    await genero_page.edit_record(validate_record=True)
    await genero_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_03 No crear con caracteres máximos en género",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_04 No crear con género vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_genero_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_05 No editar con caracteres máximos en género",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_06 No editar con género vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_genero_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_07 Crear con caracteres especiales en género",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_08 Crear con solo letras en género",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_genero_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_09 Editar con caracteres especiales en género",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_10 Editar con solo letras en género",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_genero_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_11 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldGenerosMusicalesEnum.GENERO.value,
            id="TGM_12 Filtrar por género",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.create_record()
    await genero_page.filter_by_specific_field(field)
    await genero_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_13 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_14 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_15 Habilitar género musical"),
    ],
)
@pytest.mark.asyncio
async def test_enable_genero_musical(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_16 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_17 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_18 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_19 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_20 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_21 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_22 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TGM_23 Smoke CRUD género musical"),
    ],
)
@pytest.mark.asyncio
async def test_smoke_genero_musical(login_page, user, password):
    page = await login_page(user, password)
    genero_page = PageGenerosMusicales(page)
    await genero_page.create_record()
    await genero_page.validate_record()
    await genero_page.edit_record()
    await genero_page.validate_record()
    await genero_page.delete_record()
