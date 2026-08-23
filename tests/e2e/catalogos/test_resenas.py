import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from tests.pages.usuarios.page_login import LoginPage
from pages.catalogos.page_resenas import FieldResenaEnum, PageResena

from utils.utils_functions import get_dotenv

env_config = get_dotenv()
user_admin = env_config.USER_ADMIN
password_admin = env_config.PASSWORD_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TR_01 Crear Reseña"),
    ],
)
@pytest.mark.asyncio
async def test_create_resena(page, user, password):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.create_record()
    await resena_page.validate_record()
    await resena_page.delete_record()


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldResenaEnum.ALBUM.value,
            InvalidDataType.REQUIRED,
            "Este campo es requerido",
            id="TR_04 No crear Reseña Album con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldResenaEnum.CANCION.value,
            InvalidDataType.REQUIRED,
            "Este campo es requerido",
            id="TR_05 No crear Reseña Canción con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldResenaEnum.PUNTUACION.value,
            InvalidDataType.REQUIRED,
            "Este campo es requerido",
            id="TR_06 No crear Reseña Canción con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldResenaEnum.PUNTUACION.value,
            InvalidDataType.MIN_VALUE,
            "Asegúrese de que este valor sea mayor o igual a 0.",
            id="TR_07 No crear Reseña calificación menor a 0",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldResenaEnum.PUNTUACION.value,
            InvalidDataType.MAX_VALUE,
            "Asegúrese de que este valor sea menor o igual a 10.",
            id="TR_08 No crear Reseña calificación mayor a 10",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_resena_data(page, user, password, field, validate_type, custom_error_message):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.validate_create_invalid_data(
        field_name=field, validate_type=validate_type, custom_error_message=custom_error_message
    )


@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(user_admin, password_admin, ValidDataType.LETTERS, id="TR_10 Crear reseña con números"),
    ],
)
@pytest.mark.asyncio
async def test_valid_resena_data(page, user, password, validate_data_type):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.validate_create_valid_data(FieldResenaEnum.RESENA.value, validate_data_type)


@pytest.mark.parametrize(
    "user, password, field_name",
    [
        pytest.param(user_admin, password_admin, FieldResenaEnum.ALBUM.value, id="TR_12 Filtrar Album"),
        pytest.param(user_admin, password_admin, FieldResenaEnum.CANCION.value, id="TR_13 Filtrar Cancion"),
    ],
)
@pytest.mark.asyncio
async def test_filters_resena(page, user, password, field_name):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.create_record()
    await resena_page.filter_by_specific_field(field=field_name)
    await resena_page.delete_record()


@pytest.mark.parametrize(
    "user, password", [pytest.param(user_admin, password_admin, id="TR_14 Borrar filtros de Reseñas")]
)
@pytest.mark.asyncio
async def test_clear_filters_resenas(page, user, password):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TR_15 Crear Reseña habilitar"),
    ],
)
@pytest.mark.asyncio
async def test_enable_resena(page, user, password):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TR_16 Cancelar Crear Reseña"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_resena(page, user, password):
    page = await LoginPage(page).login(user, password)
    resena_page = PageResena(page)

    await resena_page.validate_cancel_create_form_returns_to_index()
