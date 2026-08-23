import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_categoria import FieldCategoriaEnum, PageCategorias

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="CAT_01 Crear, validar y eliminar Categoría",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_categoria(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.create_record(validate_record=True)
    await categoria_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="CAT_02 Editar y validar Categoría",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_categoria(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.create_record()
    await categoria_page.edit_record(validate_record=True)
    await categoria_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_03 No crear con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_04 No crear con nombre vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_categoria_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_05 No editar con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_06 No editar con nombre vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_categoria_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_07 Crear con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_08 Crear con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_categoria_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_09 Editar con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_10 Editar con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_categoria_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_11 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldCategoriaEnum.CATEGORIA.value,
            id="CAT_12 Filtrar por nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.create_record()
    await categoria_page.filter_by_specific_field(field)
    await categoria_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_13 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_14 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_15 Habilitar categoría"),
    ],
)
@pytest.mark.asyncio
async def test_enable_categoria(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_16 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_17 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_18 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_19 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_20 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_21 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_22 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_23 Volver desde índice deshabilitado"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_disabled_index(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_back_button_on_disabled_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_24 Limpiar filtros en índice deshabilitado"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters_in_disabled_index(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_clear_filters_button_in_disabled_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_25 Filtros sin resultados en índice deshabilitado"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters_in_disabled_index(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_no_results_on_filters(disabled_index=True)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="CAT_26 Filtros vacíos en índice deshabilitado"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters_in_disabled_index(login_page, user, password):
    page = await login_page(user, password)
    categoria_page = PageCategorias(page)
    await categoria_page.validate_empty_filters(disabled_index=True)
