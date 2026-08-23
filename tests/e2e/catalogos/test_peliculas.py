from enum import Enum
import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_peliculas import FieldPeliculasEnum, PagePeliculas

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


class ErrorMessages(Enum):
    MIN_VALUE = "No mames, la primera película salió en 1895, ponte verga"
    MAX_VALUE = "Asegúrese de que este valor sea menor o igual a 2147483647."

@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="PEL_01 Crear, validar y eliminar Película",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_pelicula(login_page, user, password):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.create_record(validate_record=True)
    await pelicula_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="PEL_02 Editar y validar Película",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_pelicula(login_page, user, password):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.create_record()
    await pelicula_page.edit_record(validate_record=True)
    await pelicula_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldPeliculasEnum.TITLE.value,
            None,
            id="PEL_03 No crear con caracteres máximos en título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldPeliculasEnum.TITLE.value,
            None,
            id="PEL_04 No crear con título vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldPeliculasEnum.YEAR.value,
            None,
            id="PEL_05 No crear con año vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MIN_VALUE,
            FieldPeliculasEnum.YEAR.value,
            ErrorMessages.MIN_VALUE.value,
            id="PEL_06 No crear con año menor al mínimo",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_VALUE,
            FieldPeliculasEnum.YEAR.value,
            ErrorMessages.MAX_VALUE.value,
            id="PEL_07 No crear con año mayor al máximo",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldPeliculasEnum.GENRE.value,
            None,
            id="PEL_08 No crear con género vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldPeliculasEnum.PRICE.value,
            None,
            id="PEL_09 No crear con precio vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_pelicula_data(login_page, user, password, validate_type, field,custom_error_message):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_create_invalid_data(field, validate_type, custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldPeliculasEnum.TITLE.value,
            id="PEL_12 No editar con caracteres máximos en título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldPeliculasEnum.TITLE.value,
            id="PEL_13 No editar con título vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldPeliculasEnum.YEAR.value,
            id="PEL_14 No editar con año vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_pelicula_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldPeliculasEnum.TITLE.value,
            id="PEL_15 Crear con caracteres especiales en título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldPeliculasEnum.TITLE.value,
            id="PEL_16 Crear con solo letras en título",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_pelicula_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="PEL_17 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldPeliculasEnum.YEAR.value,
            id="PEL_20 Filtrar por año",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.create_record()
    await pelicula_page.filter_by_specific_field(field)
    await pelicula_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="PEL_21 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="PEL_22 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="PEL_23 Habilitar película"),
    ],
)
@pytest.mark.asyncio
async def test_enable_pelicula(login_page, user, password):
    page = await login_page(user, password)
    pelicula_page = PagePeliculas(page)
    await pelicula_page.validate_enable_record()
