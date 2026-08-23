import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_etiqueta_musicales import FieldEtiquetasMusicalesEnum, PageEtiquetasMusicales

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN



@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TEM_01 Crear, validar y eliminar Etiqueta musical",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_etiqueta_musical(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.create_record(validate_record=True)
    await etiqueta_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="TEM_02 Editar y validar Etiqueta musical",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_etiqueta_musical(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.create_record()
    await etiqueta_page.edit_record(validate_record=True)
    await etiqueta_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_03 No crear con caracteres máximos en etiqueta",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_04 No crear con etiqueta vacía",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_etiqueta_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_05 No editar con caracteres máximos en etiqueta",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_06 No editar con etiqueta vacía",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_etiqueta_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_07 Crear con caracteres especiales en etiqueta",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_08 Crear con solo letras en etiqueta",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_etiqueta_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_09 Editar con caracteres especiales en etiqueta",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_10 Editar con solo letras en etiqueta",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_etiqueta_musical_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_11 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEtiquetasMusicalesEnum.TAG.value,
            id="TEM_12 Filtrar por etiqueta",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.create_record()
    await etiqueta_page.filter_by_specific_field(field)
    await etiqueta_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_13 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_14 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_15 Habilitar etiqueta musical"),
    ],
)
@pytest.mark.asyncio
async def test_enable_etiqueta_musical(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_16 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_17 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_18 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_19 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_20 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_21 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_22 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="TEM_23 Smoke CRUD etiqueta musical"),
    ],
)
@pytest.mark.asyncio
async def test_smoke_etiqueta_musical(login_page, user, password):
    page = await login_page(user, password)
    etiqueta_page = PageEtiquetasMusicales(page)
    await etiqueta_page.create_record()
    await etiqueta_page.validate_record()
    await etiqueta_page.edit_record()
    await etiqueta_page.validate_record()
    await etiqueta_page.delete_record()
