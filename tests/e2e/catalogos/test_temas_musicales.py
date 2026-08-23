import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_temas_musicales import FieldTemasMusicalesEnum, PageTemasMusicales

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN

@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TTM_01 Crear, validar y eliminar Tema musical",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_tema_musical(login_page, user, password):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.create_record(validate_record=True)
    await tema_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TTM_02 Editar y validar Tema musical",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_tema_musical(login_page, user, password):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.create_record()
    await tema_page.edit_record(validate_record=True)
    await tema_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_03 No crear con caracteres máximos en tema",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_04 No crear con tema vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_tema_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_05 No editar con caracteres máximos en tema",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_06 No editar con tema vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_tema_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_07 Crear con caracteres especiales en tema",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_08 Crear con solo letras en tema",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_tema_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_09 Editar con caracteres especiales en tema",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_10 Editar con solo letras en tema",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_tema_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TTM_11 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldTemasMusicalesEnum.TEMA.value,
            id="TTM_12 Filtrar por tema",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.create_record()
    await tema_page.filter_by_specific_field(field)
    await tema_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TTM_13 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TTM_14 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    tema_page = PageTemasMusicales(page)
    await tema_page.validate_clear_filters_button()
