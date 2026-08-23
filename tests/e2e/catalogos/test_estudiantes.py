import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_estudiantes import FieldEstudianteEnum, PageEstudiantes

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EST_01 Crear, validar y eliminar Estudiante",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_estudiante(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.create_record(validate_record=True)
    await estudiante_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EST_02 Editar y validar Estudiante",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_estudiante(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.create_record()
    await estudiante_page.edit_record(validate_record=True)
    await estudiante_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEstudianteEnum.NAME.value,
            id="EST_03 No crear con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEstudianteEnum.NAME.value,
            id="EST_04 No crear con nombre vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEstudianteEnum.LAST_NAME.value,
            id="EST_05 No crear con caracteres máximos en apellido",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEstudianteEnum.LAST_NAME.value,
            id="EST_06 No crear con apellido vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEstudianteEnum.EMAIL.value,
            id="EST_07 No crear con caracteres máximos en email",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEstudianteEnum.EMAIL.value,
            id="EST_08 No crear con email vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEstudianteEnum.PHONE.value,
            id="EST_09 No crear con caracteres máximos en teléfono",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEstudianteEnum.PHONE.value,
            id="EST_10 No crear con teléfono vacío",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEstudianteEnum.ADDRESS.value,
            id="EST_11 No crear con caracteres máximos en dirección",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEstudianteEnum.ADDRESS.value,
            id="EST_12 No crear con dirección vacía",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_estudiante_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEstudianteEnum.NAME.value,
            id="EST_13 No editar con caracteres máximos en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEstudianteEnum.NAME.value,
            id="EST_14 No editar con nombre vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_estudiante_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldEstudianteEnum.NAME.value,
            id="EST_15 Crear con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldEstudianteEnum.NAME.value,
            id="EST_16 Crear con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_estudiante_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldEstudianteEnum.NAME.value,
            id="EST_17 Editar con caracteres especiales en nombre",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldEstudianteEnum.NAME.value,
            id="EST_18 Editar con solo letras en nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_estudiante_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_19 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEstudianteEnum.NAME.value,
            id="EST_20 Filtrar por nombre",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.create_record()
    await estudiante_page.filter_by_specific_field(field)
    await estudiante_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_21 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_22 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_23 Habilitar estudiante"),
    ],
)
@pytest.mark.asyncio
async def test_enable_estudiante(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_24 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_25 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_26 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_27 Botón volver en detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_detail(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_back_button_on_detail()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_28 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_29 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_30 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_31 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EST_32 Smoke CRUD estudiante"),
    ],
)
@pytest.mark.asyncio
async def test_smoke_estudiante(login_page, user, password):
    page = await login_page(user, password)
    estudiante_page = PageEstudiantes(page)
    await estudiante_page.create_record()
    await estudiante_page.validate_record()
    await estudiante_page.edit_record()
    await estudiante_page.validate_record()
    await estudiante_page.delete_record()
