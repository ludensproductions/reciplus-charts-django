import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_contenido import FieldContenidoEnum, PageContenido

from utils.utils_functions import get_dotenv

env_config = get_dotenv()
user_admin = env_config.USER_ADMIN
password_admin = env_config.PASSWORD_ADMIN


# =============================================================================
# TESTS DE CREACIÓN BÁSICA
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_01 Crear Contenido tipo Artículo"),
    ],
)
@pytest.mark.asyncio
async def test_create_contenido_articulo(login_page, user, password):
    """Test que valida la creación, validación y eliminación de un contenido tipo Artículo."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record(
        **{
            FieldContenidoEnum.TIPO_CONTENIDO.value: "Artículo",
        }
    )
    await contenido_page.validate_record()
    await contenido_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_02 Crear Contenido tipo Video"),
    ],
)
@pytest.mark.asyncio
async def test_create_contenido_video(login_page, user, password):
    """Test que valida la creación, validación y eliminación de un contenido tipo Video."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record(
        **{
            FieldContenidoEnum.TIPO_CONTENIDO.value: "Video",
        }
    )
    await contenido_page.validate_record()
    await contenido_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_03 Ver detalles de Contenido"),
    ],
)
@pytest.mark.asyncio
async def test_view_contenido_details(login_page, user, password):
    """Test que valida la visualización de detalles de un contenido."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record()
    await contenido_page.validate_record()
    await contenido_page.delete_record()


# =============================================================================
# TESTS DE VALIDACIÓN DE DATOS INVÁLIDOS - CAMPO TÍTULO
# =============================================================================


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TC_04 No crear Contenido con título excediendo caracteres máximos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_05 No crear Contenido sin título",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_titulo_create(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en el campo título durante la creación."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_create_invalid_data(field, validate_type, custom_error_message=custom_error_message)


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TC_06 No editar Contenido con título excediendo caracteres máximos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_07 No editar Contenido sin título",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_titulo_edit(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en el campo título durante la edición."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_edit_invalid_data(field, validate_type, custom_error_message=custom_error_message)


# =============================================================================
# TESTS DE VALIDACIÓN DE DATOS INVÁLIDOS - CAMPO TIPO CONTENIDO
# =============================================================================


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TIPO_CONTENIDO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_08 No crear Contenido sin tipo de contenido",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_tipo_contenido_create(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en el campo tipo de contenido durante la creación."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_create_invalid_data(field, validate_type, custom_error_message=custom_error_message)


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TIPO_CONTENIDO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_09 No editar Contenido sin tipo de contenido",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_tipo_contenido_edit(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en el campo tipo de contenido durante la edición."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_edit_invalid_data(field, validate_type, custom_error_message=custom_error_message)


# =============================================================================
# TESTS DE VALIDACIÓN DE DATOS INVÁLIDOS - CAMPOS DEPENDIENTES (ARTÍCULO)
# =============================================================================


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.CUERPO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_10 No crear Artículo sin cuerpo",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.CATEGORIA.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_11 No crear Artículo sin categoría",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_articulo_fields_create(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en campos específicos de Artículo durante la creación."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    # Primero seleccionamos tipo Artículo para activar los campos dependientes
    await contenido_page.validate_create_invalid_data(
        field,
        validate_type,
        custom_error_message=custom_error_message,
        **{FieldContenidoEnum.TIPO_CONTENIDO.value: "Artículo"},
    )


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.CUERPO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_12 No editar Artículo sin cuerpo",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.CATEGORIA.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_13 No editar Artículo sin categoría",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_articulo_fields_edit(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en campos específicos de Artículo durante la edición."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_edit_invalid_data(
        field,
        validate_type,
        custom_error_message=custom_error_message,
        **{FieldContenidoEnum.TIPO_CONTENIDO.value: "Artículo"},
    )


# =============================================================================
# TESTS DE VALIDACIÓN DE DATOS INVÁLIDOS - CAMPOS DEPENDIENTES (VIDEO)
# =============================================================================


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.URL.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_14 No crear Video sin URL",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.URL.value,
            InvalidDataType.ALPHANUMERIC,
            "Introduzca una URL válida.",
            id="TC_15 No crear Video con URL inválida",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_video_fields_create(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en campos específicos de Video durante la creación."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_create_invalid_data(
        field,
        validate_type,
        custom_error_message=custom_error_message,
        **{FieldContenidoEnum.TIPO_CONTENIDO.value: "Video"},
    )


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.URL.value,
            InvalidDataType.REQUIRED,
            None,
            id="TC_16 No editar Video sin URL",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.URL.value,
            InvalidDataType.ALPHANUMERIC,
            "Introduzca una URL válida.",
            id="TC_17 No editar Video con URL inválida",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_video_fields_edit(login_page, user, password, field, validate_type, custom_error_message):
    """Test que valida errores en campos específicos de Video durante la edición."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_edit_invalid_data(
        field,
        validate_type,
        custom_error_message=custom_error_message,
        **{FieldContenidoEnum.TIPO_CONTENIDO.value: "Video"},
    )


# =============================================================================
# TESTS DE VALIDACIÓN DE DATOS VÁLIDOS
# =============================================================================


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TC_18 Crear Contenido con caracteres especiales en título",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            ValidDataType.NUMBERS,
            id="TC_19 Crear Contenido con números en título",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            ValidDataType.LETTERS,
            id="TC_20 Crear Contenido con letras en título",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_titulo_create(login_page, user, password, field, validate_data_type):
    """Test que valida datos válidos en el campo título durante la creación."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_create_valid_data(field, validate_data_type)


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TC_21 Editar Contenido con caracteres especiales en título",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            ValidDataType.NUMBERS,
            id="TC_22 Editar Contenido con números en título",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldContenidoEnum.TITULO.value,
            ValidDataType.ALLOW_DUPLICATES,
            id="TC_23 Editar Contenido con título duplicado",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_titulo_edit(login_page, user, password, field, validate_data_type):
    """Test que valida datos válidos en el campo título durante la edición."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_edit_valid_data(field, validate_data_type)


# =============================================================================
# TESTS DE FILTROS
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_24 Filtrar Contenido por título"),
    ],
)
@pytest.mark.asyncio
async def test_filter_contenido_by_titulo(login_page, user, password):
    """Test que valida el filtrado de contenidos por título."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record()
    await contenido_page.filter_by_specific_field(FieldContenidoEnum.TITULO.value)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_26 Filtrar Contenido que no existe"),
    ],
)
@pytest.mark.asyncio
async def test_filter_contenido_no_results(login_page, user, password):
    """Test que valida que no se encuentren resultados al filtrar por un contenido inexistente."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_no_results_on_filters(field_name=FieldContenidoEnum.TITULO.value)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_27 Borrar filtros de Contenido"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters_contenido(login_page, user, password):
    """Test que valida la limpieza de filtros."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_clear_filters_button()


# =============================================================================
# TESTS DE HABILITACIÓN/DESHABILITACIÓN
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_28 Deshabilitar Contenido"),
    ],
)
@pytest.mark.asyncio
async def test_disable_contenido(login_page, user, password):
    """Test que valida la deshabilitación de un contenido."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record()
    await contenido_page.validate_record()
    await contenido_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_29 Habilitar Contenido"),
    ],
)
@pytest.mark.asyncio
async def test_enable_contenido(login_page, user, password):
    """Test que valida la habilitación de un contenido deshabilitado."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_enable_record()


# =============================================================================
# TESTS DE CANCELACIÓN
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_30 Cancelar creación de Contenido"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_contenido(login_page, user, password):
    """Test que valida la cancelación de la creación de un contenido."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_31 Cancelar edición de Contenido"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_contenido(login_page, user, password):
    """Test que valida la cancelación de la edición de un contenido."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.validate_cancel_edit_form_returns_to_index()


# =============================================================================
# TESTS DE EDICIÓN
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_32 Editar Contenido tipo Artículo"),
    ],
)
@pytest.mark.asyncio
async def test_edit_contenido_articulo(login_page, user, password):
    """Test que valida la edición de un contenido tipo Artículo."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record(**{FieldContenidoEnum.TIPO_CONTENIDO.value: "Artículo"})
    await contenido_page.edit_record()
    await contenido_page.validate_record()
    await contenido_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_33 Editar Contenido tipo Video"),
    ],
)
@pytest.mark.asyncio
async def test_edit_contenido_video(login_page, user, password):
    """Test que valida la edición de un contenido tipo Video."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record(**{FieldContenidoEnum.TIPO_CONTENIDO.value: "Video"})
    await contenido_page.edit_record()
    await contenido_page.validate_record()
    await contenido_page.delete_record()


# =============================================================================
# TESTS CON CREACIÓN DE DEPENDENCIAS
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TC_35 Crear Artículo con categoría nueva navegando"),
    ],
)
@pytest.mark.asyncio
async def test_create_articulo_with_new_category_on_page(login_page, user, password):
    """Test que valida la creación de un artículo con una categoría nueva navegando a su página."""
    page = await login_page(user, password)
    contenido_page = PageContenido(page)

    await contenido_page.create_record(
        **{
            FieldContenidoEnum.TIPO_CONTENIDO.value: "Artículo",
        },
        create_on_dependency_page=True,
    )
    await contenido_page.validate_record()
    await contenido_page.delete_record()
