import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_inventario_peliculas import FieldInventarioPeliculasEnum, PageInventarioPeliculas
from tests.pages.usuarios.page_login import LoginPage

from tests.utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="INV_PEL_9999 Validar creación."),
    ],
)
@pytest.mark.asyncio
async def test_validate_crear_inventario_peliculas(page, user, password):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.create_record()
    await page_obj.validate_record()
    await page_obj.delete_record()


@pytest.mark.parametrize(
    "user, password, field, validation_type, custom_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.QUANTITY.value,
            InvalidDataType.LETTERS,
            None,
            id="INV_PEL_9998 Validar creación.",
        ),
    ],
)
@pytest.mark.asyncio
async def test_validate_crear_inventario_peliculas1(page, user, password, field, validation_type, custom_message):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_create_invalid_data(field, validation_type, custom_error_message=custom_message)


@pytest.mark.parametrize(
    "user, password, field, validation_type",
    [
        # pytest.param(
        #     admin_user,
        #     admin_password,
        #     FieldInventarioPeliculasEnum.PHONE.value,
        #     ValidDataType.DISABLED,
        #     id="INV_PEL_9997 Validar creación."
        # ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.PRODUCTOR.value,
            ValidDataType.NUMBERS,
            id="INV_PEL_9996 Validar creación.",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.PRODUCTOR.value,
            ValidDataType.SPECIAL_CHARS,
            id="INV_PEL_9995 Validar creación.",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.PRODUCTOR.value,
            ValidDataType.LETTERS,
            id="INV_PEL_9994 Validar creación.",
        ),
        # pytest.param(
        #     admin_user,
        #     admin_password,
        #     FieldInventarioPeliculasEnum.PRODUCTOR.value,
        #     ValidDataType.NEGATIVE_NUMBER,
        #     id="INV_PEL_9993 Validar creación."
        # ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.PRODUCTOR.value,
            ValidDataType.ALPHANUMERIC,
            id="INV_PEL_9992 Validar creación.",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.REGISTRATION_DATE.value,
            ValidDataType.DATE_DD_MM_YYYY,
            id="INV_PEL_9991 Validar creación.",
        ),
        # pytest.param(
        #     admin_user,
        #     admin_password,
        #     FieldInventarioPeliculasEnum.PRODUCTOR.value,
        #     ValidDataType.DECIMAL,
        #     id="INV_PEL_9990 Validar creación."
        # ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.BILLING_FILE.value,
            ValidDataType.VALID_FORMAT,
            id="INV_PEL_9989 Validar creación.",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldInventarioPeliculasEnum.PRODUCTOR.value,
            ValidDataType.ALLOW_DUPLICATES,
            id="INV_PEL_9988 Validar creación.",
        ),
        # pytest.param(
        #     admin_user,
        #     admin_password,
        #     FieldInventarioPeliculasEnum.PRODUCTOR.value,
        #     ValidDataType.EMPTY,
        #     id="INV_PEL_9987 Validar creación."
        # ),
    ],
)
@pytest.mark.asyncio
async def test_validate_crear_inventario_peliculas11(page, user, password, field, validation_type):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_create_valid_data(field, validation_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="INV_PEL_9986 Validar habilitación."),
    ],
)
@pytest.mark.asyncio
async def test_validate_habilitar_inventario_peliculas(page, user, password):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="INV_PEL_9985 Validar botón borrar filtros."),
    ],
)
@pytest.mark.asyncio
async def test_validate_borrar_filtros_inventario_peliculas(page, user, password):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_clear_filters_button_in_disabled_index()


# validar filtros invalidas
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="INV_PEL_9984 Validar filtros invalidos."),
    ],
)
@pytest.mark.asyncio
async def test_validate_filtros_invalidos_inventario_peliculas(page, user, password):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_no_results_on_filters(disabled_index=True)


# validar filtros vacios
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="INV_PEL_9983 Validar filtros vacios."),
    ],
)
@pytest.mark.asyncio
async def test_validate_filtros_vacios_inventario_peliculas(page, user, password):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_empty_filters(disabled_index=True)


# validar filtros vacios
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="INV_PEL_94994 Cancelar modal de habilitacion."),
    ],
)
@pytest.mark.asyncio
async def test_validate_cancelar_modal_habilitacion_inventario_peliculas(page, user, password):
    page = await LoginPage(page, user, password).login()
    page_obj = PageInventarioPeliculas(page)
    await page_obj.validate_cancel_enable_modal()
