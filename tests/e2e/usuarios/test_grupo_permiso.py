from enum import Enum

import pytest
from pages.catalogos.page_grupo_permiso import FieldGrupoPermisoEnum, PageGrupoPermiso
from tests.pages.core.constants import InvalidDataType, ValidDataType
from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


class ErrorMessages(Enum):
    """Mensajes de error esperados para grupos."""

    DUPLICATED = "Ya existe un grupo con esta clave."
    INVALID_NAME = "Ingrese un grupo válido. Solo se aceptan letras y números."


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_01 Crear, validar y eliminar Grupo de permisos"),
    ],
)
@pytest.mark.asyncio
async def test_create_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.create_record(validate_record=True)
    await grupo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_02 Editar y validar Grupo de permisos"),
    ],
)
@pytest.mark.asyncio
async def test_edit_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.create_record()
    await grupo_page.edit_record(validate_record=True)
    await grupo_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            None,
            id="GRP_03 No crear grupo con display_name excediendo longitud máxima",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            None,
            id="GRP_04 No crear grupo sin display_name",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.DUPLICATED,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            ErrorMessages.DUPLICATED.value,
            id="GRP_05 No crear grupo con display_name duplicado",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.NO_SPECIAL_CHARS,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            ErrorMessages.INVALID_NAME.value,
            id="GRP_06 No crear grupo con caracteres inválidos en display_name",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_grupo_permiso_data(
    login_page, user, password, validate_type, field, custom_error_message
):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_create_invalid_data(field, validate_type, custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field, custom_error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            None,
            id="GRP_07 No editar grupo con display_name excediendo longitud máxima",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            None,
            id="GRP_08 No editar grupo sin display_name",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.DUPLICATED,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            ErrorMessages.DUPLICATED.value,
            id="GRP_09 No editar grupo con display_name duplicado",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.NO_SPECIAL_CHARS,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            ErrorMessages.INVALID_NAME.value,
            id="GRP_10 No editar grupo con caracteres inválidos en display_name",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_grupo_permiso_data(login_page, user, password, validate_type, field, custom_error_message):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_edit_invalid_data(field, validate_type, custom_error_message)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            id="GRP_11 Crear grupo con display_name válido (solo letras)",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_create_grupo_permiso_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.ALPHANUMERIC,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            id="GRP_12 Editar grupo con display_name válido (alfanumérico)",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_grupo_permiso_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldGrupoPermisoEnum.DISPLAY_NAME.value,
            id="GRP_13 Filtrar grupos por display_name",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_grupo_permiso_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.create_record()
    await grupo_page.filter_by_specific_field(field)
    await grupo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_14 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_grupo_permiso_filters(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_15 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_grupo_permiso_filters(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_16 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_grupo_permiso_filters(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_17 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_grupo_permiso_form(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_18 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_grupo_permiso_form(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_19 Cancelar modal de deshabilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_20 Habilitar grupo"),
    ],
)
@pytest.mark.asyncio
async def test_enable_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_21 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_22 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_grupo_permiso_without_changes(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_23 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_24 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit_grupo_permiso(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_25 Crear grupo asignando permiso"),
    ],
)
@pytest.mark.asyncio
async def test_create_grupo_permiso_with_permission(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.create_record_with_permission(validate_record=True)
    await grupo_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_26 Editar grupo agregando permiso"),
    ],
)
@pytest.mark.asyncio
async def test_edit_grupo_permiso_add_permission(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_edit_add_permission()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="GRP_27 Editar grupo quitando permiso"),
    ],
)
@pytest.mark.asyncio
async def test_edit_grupo_permiso_remove_permission(login_page, user, password):
    page = await login_page(user, password)
    grupo_page = PageGrupoPermiso(page)
    await grupo_page.validate_edit_remove_permission()
