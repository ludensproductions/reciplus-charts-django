import pytest
from pages.catalogos.page_tipo_vehiculo import FieldTipoVehiculoEnum, PageTipoVehiculo
from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN

from tests.pages.core.constants import InvalidDataType, ValidDataType


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TTV_01 Crear, validar y eliminar Tipo vehículo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_tipo_vehiculo(login_page, user, password):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.create_record(validate_record=True)
    await tipo_vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TTV_02 Editar y validar Tipo vehículo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_tipo_vehiculo(login_page, user, password):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.create_record()
    await tipo_vehiculo_page.edit_record(validate_record=True)
    await tipo_vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_03 No crear con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_04 No crear con nombre vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_tipo_vehiculo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_05 No editar con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_06 No editar con nombre vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_tipo_vehiculo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_07 Crear con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_08 Crear con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_tipo_vehiculo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_09 Editar con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_10 Editar con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_tipo_vehiculo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TTV_11 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldTipoVehiculoEnum.NOMBRE.value,
            id="TTV_12 Filtrar por nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.create_record()
    await tipo_vehiculo_page.filter_by_specific_field(field)
    await tipo_vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TTV_13 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TTV_14 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    tipo_vehiculo_page = PageTipoVehiculo(page)
    await tipo_vehiculo_page.validate_clear_filters_button()
