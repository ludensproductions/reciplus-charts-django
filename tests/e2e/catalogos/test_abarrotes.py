"""Tests E2E para el módulo de Abarrotes."""

import pytest
from pages.catalogos.page_abarrotes import FieldAbarrotesEnum, PageAbarrotes
from tests.pages.core.constants import InvalidDataType, ValidDataType

from tests.utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


# =============================================================================
# CRUD Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_01 Crear abarrote"),
    ],
)
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_create_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.create_record()
    await abarrotes_page.validate_record()
    await abarrotes_page.delete_record()


# =============================================================================
# Invalid Data Tests - CREATE
# =============================================================================
@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TAB_02 No crear abarrote con caracteres máximos permitidos",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_03 No crear abarrote con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.PRODUCTO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_04 No crear abarrote sin producto",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            InvalidDataType.MIN_VALUE,
            "Asegúrese de que este valor sea mayor o igual a 0.",
            id="TAB_05 No crear abarrote con cantidad menor a 0",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            InvalidDataType.MAX_VALUE,
            "Asegúrese de que este valor sea menor o igual a 2147483647.",
            id="TAB_06 No crear abarrote con cantidad mayor al máximo permitido",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_07 No crear abarrote sin cantidad",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.FECHA.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_08 No crear abarrote sin fecha",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_abarrotes_data(
    login_page,
    user,
    password,
    field,
    validate_type,
    custom_error_message,
):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_create_invalid_data(
        field_name=field,
        validate_type=validate_type,
        custom_error_message=custom_error_message,
    )


# =============================================================================
# Invalid Data Tests - EDIT
# =============================================================================
@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TAB_09 No editar abarrote con caracteres máximos permitidos",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_10 No editar abarrote con campo vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.PRODUCTO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_11 No editar abarrote sin producto",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            InvalidDataType.MIN_VALUE,
            "Asegúrese de que este valor sea mayor o igual a 0.",
            id="TAB_12 No editar abarrote con cantidad menor a 0",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            InvalidDataType.MAX_VALUE,
            "Asegúrese de que este valor sea menor o igual a 2147483647.",
            id="TAB_13 No editar abarrote con cantidad mayor al máximo permitido",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_14 No editar abarrote sin cantidad",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.FECHA.value,
            InvalidDataType.REQUIRED,
            None,
            id="TAB_15 No editar abarrote sin fecha",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_abarrotes_data(
    login_page,
    user,
    password,
    field,
    validate_type,
    custom_error_message,
):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_edit_invalid_data(
        field_name=field,
        validate_type=validate_type,
        custom_error_message=custom_error_message,
    )


# =============================================================================
# Valid Data Tests - CREATE
# =============================================================================
@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            ValidDataType.LETTERS,
            id="TAB_16 Crear abarrote con solo letras",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            ValidDataType.NUMBERS,
            id="TAB_17 Crear abarrote con cantidad numérica válida",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_create_abarrotes_data(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_create_valid_data(
        field_name=field,
        validate_data_type=validate_data_type,
    )


# =============================================================================
# Valid Data Tests - EDIT
# =============================================================================
@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            ValidDataType.LETTERS,
            id="TAB_18 Editar abarrote con solo letras",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            ValidDataType.NUMBERS,
            id="TAB_19 Editar abarrote con cantidad numérica válida",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_abarrotes_data(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_edit_valid_data(
        field_name=field,
        validate_data_type=validate_data_type,
    )


# =============================================================================
# Filter Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password, field_name",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            id="TAB_20 Filtrar abarrote por nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.PRODUCTO.value,
            id="TAB_21 Filtrar abarrote por producto",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            id="TAB_22 Filtrar abarrote por cantidad",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.FECHA.value,
            id="TAB_23 Filtrar abarrote por fecha",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filters_abarrotes(login_page, user, password, field_name):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.create_record()
    await abarrotes_page.filter_by_specific_field(field=field_name)
    await abarrotes_page.delete_record()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.ABARROTES.value,
            id="TAB_24 Filtrar abarrote que no existe por nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldAbarrotesEnum.CANTIDAD.value,
            id="TAB_25 Filtrar abarrote que no existe por cantidad",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_filter_abarrotes(login_page, user, password, field):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_no_results_on_filters(field_name=field)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_26 Borrar filtros de abarrotes")],
)
@pytest.mark.asyncio
async def test_clear_filters_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_27 Validar filtros vacíos")],
)
@pytest.mark.asyncio
async def test_empty_filters_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_empty_filters()


# =============================================================================
# Enable/Disable Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_28 Habilitar abarrote"),
    ],
)
@pytest.mark.asyncio
async def test_enable_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.create_record()
    await abarrotes_page.delete_record(delete_dependencies=False)
    await abarrotes_page.enable_record()
    await abarrotes_page.validate_record()
    await abarrotes_page.delete_record(delete_dependencies=False)


# =============================================================================
# Navigation Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_29 Cancelar crear abarrote"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_30 Cancelar editar abarrote"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_31 Botón volver en crear"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_32 Botón volver en editar"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_33 Botón volver en detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_detail_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_back_button_on_detail()


# =============================================================================
# Edit Without Changes
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_34 Editar abarrote sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_edit_without_changes()


# =============================================================================
# Modal Tests
# =============================================================================
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_35 Cancelar modal de eliminar"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TAB_36 Cancelar modal de habilitar"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal_abarrotes(login_page, user, password):
    page = await login_page(user, password)
    abarrotes_page = PageAbarrotes(page)

    await abarrotes_page.validate_cancel_enable_modal()
