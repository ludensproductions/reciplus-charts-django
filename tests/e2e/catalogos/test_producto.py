import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from tests.pages.usuarios.page_login import LoginPage
from pages.catalogos.page_producto import FieldProductosEnum, PageProducto

from utils.utils_functions import get_dotenv

env_config = get_dotenv()
user_admin = env_config.USER_ADMIN
password_admin = env_config.PASSWORD_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TP_01 Crear  producto"),
        pytest.param(user_admin, password_admin, id="TP_02 Ver detalles de  producto"),
        pytest.param(user_admin, password_admin, id="TP_03 Crear producto deshabilitar"),
    ],
)
@pytest.mark.asyncio
async def test_create_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.create_record()
    await producto_page.validate_record()
    await producto_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.REQUIRED,
            "Este campo es requerido",
            id="TP_04 No crear producto con campo vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_producto_data(page, user, password, validate_type, custom_error_message):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_create_invalid_data(
        FieldProductosEnum.PRODUCTO.value,
        validate_type,
        custom_error_message=custom_error_message,
    )


@pytest.mark.parametrize(
    "user, password, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.REQUIRED,
            None,
            id="TP_05 No crear producto con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.DUPLICATED,
            "Ya existe un/a Producto con este/a Producto.",
            id="TP_35 No crear producto con campo duplicado",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_producto_data(page, user, password, validate_type, custom_error_message):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_edit_invalid_data(
        FieldProductosEnum.PRODUCTO.value,
        validate_type,
        custom_error_message=custom_error_message,
    )


@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            ValidDataType.SPECIAL_CHARS,
            id="TP_06 Crear producto con caracteres especiales",
        ),
        pytest.param(user_admin, password_admin, ValidDataType.LETTERS, id="TP_07 Crear producto con números"),
    ],
)
@pytest.mark.asyncio
async def test_valid_producto_data(page, user, password, validate_data_type):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_create_valid_data(FieldProductosEnum.PRODUCTO.value, validate_data_type)


@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            ValidDataType.SPECIAL_CHARS,
            id="TP_08 Crear producto con caracteres especiales",
        ),
        pytest.param(user_admin, password_admin, ValidDataType.LETTERS, id="TP_09 Crear producto con números"),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_producto_data(page, user, password, validate_data_type):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_edit_valid_data(FieldProductosEnum.PRODUCTO.value, validate_data_type)


@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            ValidDataType.ALLOW_DUPLICATES,
            id="TP_33 Crear producto con valores duplicados",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_tipo_producto_data(page, user, password, validate_data_type):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_edit_valid_data(FieldProductosEnum.TIPO_PRODUCTO.value, validate_data_type)


@pytest.mark.parametrize(
    "user, password,",
    [
        pytest.param(user_admin, password_admin, id="TP_10 Filtrar  producto"),
    ],
)
@pytest.mark.asyncio
async def test_filters_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.create_record()
    await producto_page.filter_by_specific_field(FieldProductosEnum.PRODUCTO.value)
    await producto_page.delete_record()


@pytest.mark.parametrize(
    "user, password", [pytest.param(user_admin, password_admin, id="TP_11 Filtrar producto que no existe")]
)
@pytest.mark.asyncio
async def test_invalid_filter_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_no_results_on_filters(field_name=FieldProductosEnum.PRODUCTO.value)


@pytest.mark.parametrize(
    "user, password", [pytest.param(user_admin, password_admin, id="TP_12 Borrar filtros de  producto")]
)
@pytest.mark.asyncio
async def test_clear_filters_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TP_13 Crear producto habilitar"),
    ],
)
@pytest.mark.asyncio
async def test_enable_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TP_14 Cancelar Crear  producto"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    producto_page = PageProducto(page)

    await producto_page.validate_cancel_create_form_returns_to_index()
