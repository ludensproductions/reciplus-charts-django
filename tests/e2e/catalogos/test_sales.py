import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from tests.pages.usuarios.page_login import LoginPage
from pages.catalogos.page_sales import FieldsVentasEnum, PageSales

from tests.utils.user_constants import USER_ADMIN, PASSWORD_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_01 Crear Ventas"),
    ],
)
@pytest.mark.asyncio
async def test_create_sales(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.create_record()
    await sales_page.validate_record()
    await sales_page.delete_record()


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.NAME.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TS_04 No crear Ventas con caracteres máximos permitidos",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.NAME.value,
            InvalidDataType.REQUIRED,
            None,
            id="TS_05 No crear Ventas con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.MOVIE.value,
            InvalidDataType.REQUIRED,
            None,
            id="TS_08 No crear Ventas con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.QUANTITY.value,
            InvalidDataType.REQUIRED,
            None,
            id="TS_09 No crear Ventas con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.QUANTITY.value,
            InvalidDataType.MAX_VALUE,
            "Asegúrese de que este valor sea menor o igual a 2147483647.",
            id="TS_11 No crear Ventas con cantidad mayor al máximo permitido",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_sales_data(page, user, password, field, validate_type, custom_error_message):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_create_invalid_data(
        field_name=field, validate_type=validate_type, custom_error_message=custom_error_message
    )




@pytest.mark.parametrize(
    "user, password, field, validate_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.NAME.value,
            ValidDataType.LETTERS,
            id="TS_12 Crear Ventas con nombre solo letras",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.NAME.value,
            ValidDataType.SPECIAL_CHARS,
            id="TS_13 Crear Ventas con nombre con caracteres especiales",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.NAME.value,
            ValidDataType.ALPHANUMERIC,
            id="TS_14 Crear Ventas con nombre alfanumérico",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_sales_data(page, user, password, field, validate_type):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_create_valid_data(field, validate_type)




@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldsVentasEnum.NAME.value,
            id="TS_15 Filtrar Ventas por nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_sales(page, user, password, field):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.create_record()
    await sales_page.filter_by_specific_field(field)
    await sales_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_16 Filtros sin resultados en Ventas"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_17 Limpiar filtros en Ventas"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_18 Filtros vacíos en Ventas"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_empty_filters()




@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_19 Cancelar formulario de creación regresa al índice"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_20 Botón volver en formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_21 Botón volver en vista de detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_detail(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_back_button_on_detail()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_22 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.validate_cancel_delete_modal()






@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TS_24 Smoke Ventas: crear, validar y eliminar"),
    ],
)
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_smoke_sales(page, user, password):
    page = await LoginPage(page).login(user, password)
    sales_page = PageSales(page)

    await sales_page.create_record()
    await sales_page.validate_record()
    await sales_page.delete_record()
