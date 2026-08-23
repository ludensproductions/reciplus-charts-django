from enum import Enum

import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_vehiculo import FieldVehiculoEnum, PageVehiculo

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


class ErrorMessages(Enum):
    MIN_LENGTH_PLACA = "Asegúrese de que este valor tenga como mínimo 4 caracteres"
    ANIO_INVALIDO = "Ingrese un año válido"
    PLACA_DUPLICADA = "Ya existe un/a Vehículo con este/a Placa."


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="VEH_01 Crear, validar y eliminar Vehículo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_vehiculo(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.create_record(validate_record=True)
    await vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="VEH_02 Editar y validar Vehículo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_vehiculo(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.create_record()
    await vehiculo_page.edit_record(validate_record=True)
    await vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="VEH_03 Editar sin cambios Vehículo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes_vehiculo(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldVehiculoEnum.PLACA.value,
            None,
            id="VEH_04 No crear con caracteres máximos en placa",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldVehiculoEnum.PLACA.value,
            None,
            id="VEH_05 No crear con placa vacía",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MIN_LENGTH,
            FieldVehiculoEnum.PLACA.value,
            ErrorMessages.MIN_LENGTH_PLACA.value,
            id="VEH_06 No crear con placa menor a 4 caracteres",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldVehiculoEnum.MODELO.value,
            None,
            id="VEH_07 No crear con modelo muy largo",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldVehiculoEnum.MODELO.value,
            None,
            id="VEH_08 No crear con modelo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_VALUE,
            FieldVehiculoEnum.ANIO.value,
            ErrorMessages.ANIO_INVALIDO.value,
            id="VEH_09 No crear con año mayor a 2100",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MIN_VALUE,
            FieldVehiculoEnum.ANIO.value,
            ErrorMessages.ANIO_INVALIDO.value,
            id="VEH_10 No crear con año menor a 1900",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.DUPLICATED,
            FieldVehiculoEnum.PLACA.value,
            ErrorMessages.PLACA_DUPLICADA.value,
            id="VEH_11 No crear con placa duplicada",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_vehiculo_data(login_page, user, password, validate_type, field, custom_error_message):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_create_invalid_data(field, validate_type, custom_error_message=custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldVehiculoEnum.PLACA.value,
            None,
            id="VEH_12 No editar con caracteres máximos en placa",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldVehiculoEnum.PLACA.value,
            None,
            id="VEH_13 No editar con placa vacía",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MIN_LENGTH,
            FieldVehiculoEnum.PLACA.value,
            ErrorMessages.MIN_LENGTH_PLACA.value,
            id="VEH_14 No editar con placa menor a 4 caracteres",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.DUPLICATED,
            FieldVehiculoEnum.PLACA.value,
            ErrorMessages.PLACA_DUPLICADA.value,
            id="VEH_55 No editar con placa duplicada",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_vehiculo_data(login_page, user, password, validate_type, field, custom_error_message):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_edit_invalid_data(field, validate_type, custom_error_message=custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldVehiculoEnum.MODELO.value,
            id="VEH_15 Crear con caracteres especiales en modelo",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldVehiculoEnum.MODELO.value,
            id="VEH_16 Crear con solo letras en modelo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_vehiculo_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_17 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_18 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_19 Volver en formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_20 Volver en formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_21 Volver en página de detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_detail(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_back_button_on_detail()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldVehiculoEnum.PLACA.value,
            id="VEH_22 Filtrar por placa",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.create_record()
    await vehiculo_page.filter_by_specific_field(field)
    await vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_24 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_25 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_26 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="VEH_27 Cancelar modal de eliminar"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    vehiculo_page = PageVehiculo(page)
    await vehiculo_page.validate_cancel_delete_modal()
