"""Tests E2E para el módulo de marcas de vehículos."""

import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_marca_vehiculo import FieldMarcaVehiculoEnum, PageMarcaVehiculo

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


# =============================================================================
# CRUD Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_01 Crear Marca de vehículo"),
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_02 Ver detalles de Marca de vehículo"),
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_03 Editar Marca de vehículo"),
    ],
)
@pytest.mark.asyncio
async def test_create_marca_vehiculo(login_page, user, password):
    """Valida el flujo completo CRUD de marca de vehículo."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.create_record()
    await marca_vehiculo_page.validate_record()
    await marca_vehiculo_page.delete_record()


# =============================================================================
# Invalid Data Tests - CREATE
# =============================================================================
@pytest.mark.parametrize(
    "user, password, validate_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            id="MVH_04 No crear Marca de vehículo con caracteres máximos permitidos",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            id="MVH_05 No crear Marca de vehículo con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MIN_LENGTH,
            id="MVH_06 No crear Marca de vehículo con menos de 2 caracteres",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_marca_vehiculo_data(login_page, user, password, validate_type):
    """Valida que datos inválidos no permitan crear una marca de vehículo."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)
    await marca_vehiculo_page.validate_create_invalid_data(FieldMarcaVehiculoEnum.NOMBRE.value, validate_type)


# =============================================================================
# Invalid Data Tests - EDIT
# =============================================================================
@pytest.mark.parametrize(
    "user, password, validate_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            id="MVH_07 No editar Marca de vehículo con caracteres máximos",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            id="MVH_08 No editar Marca de vehículo con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MIN_LENGTH,
            id="MVH_09 No editar Marca de vehículo con menos de 2 caracteres",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_marca_vehiculo_data(login_page, user, password, validate_type):
    """Valida que datos inválidos no permitan editar una marca de vehículo."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_edit_invalid_data(
        field_name=FieldMarcaVehiculoEnum.NOMBRE.value,
        validate_type=validate_type,
    )


# =============================================================================
# Valid Data Tests - CREATE
# =============================================================================
@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            id="MVH_10 Crear Marca de vehículo con caracteres especiales",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            id="MVH_11 Crear Marca de vehículo con solo letras",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_marca_vehiculo_data(login_page, user, password, validate_data_type):
    """Valida que datos válidos permitan crear una marca de vehículo."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_create_valid_data(FieldMarcaVehiculoEnum.NOMBRE.value, validate_data_type)


# =============================================================================
# Valid Data Tests - EDIT
# =============================================================================
@pytest.mark.parametrize(
    "user, password, validate_data_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            id="MVH_12 Editar Marca de vehículo con caracteres especiales",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            id="MVH_13 Editar Marca de vehículo con solo letras",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_marca_vehiculo_data(login_page, user, password, validate_data_type):
    """Valida que datos válidos permitan editar una marca de vehículo."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_edit_valid_data(FieldMarcaVehiculoEnum.NOMBRE.value, validate_data_type)


# =============================================================================
# Filter Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_14 Filtrar Marca de vehículo"),
    ],
)
@pytest.mark.asyncio
async def test_filters_marca_vehiculo(login_page, user, password):
    """Valida que el filtro por campo específico funcione correctamente."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.create_record()
    await marca_vehiculo_page.filter_by_specific_field(FieldMarcaVehiculoEnum.NOMBRE.value)
    await marca_vehiculo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_15 Filtrar Marca de vehículo que no existe")],
)
@pytest.mark.asyncio
async def test_invalid_filter_marca_vehiculo(login_page, user, password):
    """Valida que el filtro no muestre resultados cuando no existen coincidencias."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_no_results_on_filters(field_name=FieldMarcaVehiculoEnum.NOMBRE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_16 Borrar filtros de Marca de vehículo")],
)
@pytest.mark.asyncio
async def test_clear_filters_marca_vehiculo(login_page, user, password):
    """Valida que el botón limpiar filtros funcione correctamente."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_24 Filtrar con campos vacíos")],
)
@pytest.mark.asyncio
async def test_empty_filters_marca_vehiculo(login_page, user, password):
    """Valida que los filtros vacíos no causen errores en la URL."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_empty_filters()


# =============================================================================
# Navigation Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_17 Cancelar Crear Marca de vehículo"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_marca_vehiculo(login_page, user, password):
    """Valida que cancelar en crear regrese al índice."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_18 Cancelar Editar Marca de vehículo"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_marca_vehiculo(login_page, user, password):
    """Valida que cancelar en editar regrese al índice."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_19 Botón volver en crear"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create_marca_vehiculo(login_page, user, password):
    """Valida que el botón volver en crear regrese al índice."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_20 Botón volver en editar"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit_marca_vehiculo(login_page, user, password):
    """Valida que el botón volver en editar regrese al índice."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_21 Botón volver en detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_detail_marca_vehiculo(login_page, user, password):
    """Valida que el botón volver en detalle regrese al índice."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_back_button_on_detail()


# =============================================================================
# Edit Without Changes Test
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_22 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes_marca_vehiculo(login_page, user, password):
    """Valida que editar sin cambios guarde correctamente."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_edit_without_changes()


# =============================================================================
# Modal Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="MVH_23 Cancelar modal de eliminar"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal_marca_vehiculo(login_page, user, password):
    """Valida que cancelar en el modal de eliminar no elimine el registro."""
    page = await login_page(user, password)
    marca_vehiculo_page = PageMarcaVehiculo(page)

    await marca_vehiculo_page.validate_cancel_delete_modal()
