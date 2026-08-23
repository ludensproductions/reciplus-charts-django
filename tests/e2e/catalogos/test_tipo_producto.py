import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from tests.pages.usuarios.page_login import LoginPage

from tests.pages.catalogos.page_tipo_producto import FieldTipoProductoEnum, PageTipoProducto
from utils.utils_functions import get_dotenv

env_config = get_dotenv()
user_admin = env_config.USER_ADMIN
password_admin = env_config.PASSWORD_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TTP_01 Crear Tipo producto"),
        pytest.param(user_admin, password_admin, id="TTP_02 Ver detalles de Tipo producto"),
        pytest.param(user_admin, password_admin, id="TTP_03 Crear Tipo producto deshabilitar"),
    ],
)
@pytest.mark.asyncio
async def test_create_tipo_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.create_record()
    await tipo_producto_page.validate_record()
    await tipo_producto_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.MAX_LENGTH,
            "Asegúrese de que este valor tenga como máximo 255 caracteres (tiene 256).",
            id="TTP_04 No crear Tipo producto con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.REQUIRED,
            "Este campo es requerido",
            id="TTP_05 No crear Tipo producto con campo vacío",
        ),
        # pytest.param(
        #     user_admin,
        #     password_admin,
        #     InvalidDataType.DUPLICATED,
        #     "Este campo es requerido",
        #     id="TTP_15 No crear Tipo producto duplicado",
        # ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_tipo_producto_data(page, user, password, validate_type, custom_error_message):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_create_invalid_data(
        FieldTipoProductoEnum.NOMBRE.value,
        validate_type,
        custom_error_message=custom_error_message,
    )


@pytest.mark.parametrize(
    "user, password, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.MAX_LENGTH,
            "Asegúrese de que este valor tenga como máximo 255 caracteres (tiene 256).",
            id="TTP_06 No crear Tipo producto con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            InvalidDataType.REQUIRED,
            "Este campo es requerido",
            id="TTP_07 No crear Tipo producto con campo vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_tipo_producto_data(page, user, password, validate_type, custom_error_message):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_edit_invalid_data(
        FieldTipoProductoEnum.NOMBRE.value,
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
            id="TTP_08 Crear Tipo producto con caracteres especiales",
        ),
        pytest.param(user_admin, password_admin, ValidDataType.LETTERS, id="TTP_09 Crear Tipo producto con números"),
    ],
)
@pytest.mark.asyncio
async def test_valid_tipo_producto_data(page, user, password, validate_data_type):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_create_valid_data(FieldTipoProductoEnum.NOMBRE.value, validate_data_type)


@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            ValidDataType.SPECIAL_CHARS,
            id="TTP_10 Crear Tipo producto con caracteres especiales",
        ),
        pytest.param(user_admin, password_admin, ValidDataType.LETTERS, id="TTP_11 Crear Tipo producto con números"),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_tipo_producto_data(page, user, password, validate_data_type):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_edit_valid_data(FieldTipoProductoEnum.NOMBRE.value, validate_data_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TTP_12 Filtrar Tipo producto"),
    ],
)
@pytest.mark.asyncio
async def test_filters_tipo_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.create_record()
    await tipo_producto_page.filter_by_specific_field(FieldTipoProductoEnum.NOMBRE.value)
    await tipo_producto_page.delete_record()


@pytest.mark.parametrize(
    "user, password", [pytest.param(user_admin, password_admin, id="TTP_13 Filtrar Tipo producto que no existe")]
)
@pytest.mark.asyncio
async def test_invalid_filter_tipo_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_no_results_on_filters(field_name=FieldTipoProductoEnum.NOMBRE.value)


@pytest.mark.parametrize(
    "user, password", [pytest.param(user_admin, password_admin, id="TTP_14 Borrar filtros de Tipo producto")]
)
@pytest.mark.asyncio
async def test_clear_filters_tipo_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TTP_15 Crear Tipo producto habilitar"),
    ],
)
@pytest.mark.asyncio
async def test_enable_tipo_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TTP_16 Cancelar Crear Tipo producto"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_tipo_producto(page, user, password):
    page = await LoginPage(page).login(user, password)
    tipo_producto_page = PageTipoProducto(page)

    await tipo_producto_page.validate_cancel_create_form_returns_to_index()
