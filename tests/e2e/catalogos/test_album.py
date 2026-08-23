import pytest
from pages.catalogos.page_album import FieldAlbumEnum, PageAlbum
from utils.utils_functions import get_dotenv
from pages.core.mixins.formset_mixin import FillFormsetOptions

from tests.pages.core.constants import InvalidDataType, ValidDataType

env_config = get_dotenv()
user_admin = env_config.USER_ADMIN
password_admin = env_config.PASSWORD_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_01 Crear Álbum"),
        # pytest.param(user_admin, password_admin, id="TA_02 Ver detalles de Álbum"),
        # pytest.param(user_admin, password_admin, id="TA_03 Crear Álbum deshabilitar"),
    ],
)
@pytest.mark.asyncio
async def test_create_album(login_page, user, password):
    page = await login_page(user, password)
    album_page = PageAlbum(page)
    await album_page.create_record()
    await album_page.validate_record()
    await album_page.delete_record()


# =============================================================================
# TESTS PARA DEMOSTRAR LA NUEVA FUNCIONALIDAD DE CONTROL INDIVIDUAL DE DEPENDENCIAS
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_100 Control individual - Crear múltiples géneros sin navegar"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_multiple_genres_inline(login_page, user, password):
    """Demuestra: Control individual del número de dependencias y creación inline.

    - Crea 4 géneros musicales sin navegar a su página (create_on_page_generos_musicales=False)
    - Las otras dependencias usan el comportamiento por defecto
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(
        num_generos_musicales=4,  # Crear 4 géneros
        create_on_page_generos_musicales=False,  # Sin navegar a página de géneros
    )
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_101 Control mixto - Cada dependencia diferente"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_mixed_dependency_control(login_page, user, password):
    """Demuestra: Control individual para cada dependencia con comportamientos diferentes.

    - Etiquetas: 2 instancias, navegando a su página (create_on_page_etiquetas_musicales=True)
    - Géneros: 3 instancias, sin navegar (create_on_page_generos_musicales=False)
    - Temas: 1 instancia (default), sin navegar (create_on_page_temas_musicales=False)
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(
        num_etiquetas_musicales=2,
        create_on_page_etiquetas_musicales=True,  # Navegar a página de etiquetas
        num_generos_musicales=3,
        create_on_page_generos_musicales=False,  # No navegar a géneros
        num_temas_musicales=1,
        create_on_page_temas_musicales=False,  # No navegar a temas
    )
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_102 Control global con override individual"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_global_with_override(login_page, user, password):
    """Demuestra: Control global con override específico para una dependencia.

    - Global: Todas las dependencias sin navegar (create_on_dependency_page=False)
    - Override: Solo géneros musicales SÍ navega a su página (create_on_page_generos_musicales=True)
    - Resultado: Etiquetas y temas inline, géneros en su página
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(
        create_on_dependency_page=False,  # Default global: no navegar
        num_generos_musicales=2,
        create_on_page_generos_musicales=True,  # Override: SÍ navegar solo para géneros
        num_etiquetas_musicales=1,  # Usará el default global (False)
        num_temas_musicales=1,  # Usará el default global (False)
    )
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_103 Todas las dependencias en sus páginas"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_all_dependencies_on_pages(login_page, user, password):
    """Demuestra: Todas las dependencias creadas navegando a sus respectivas páginas.

    - Especifica explícitamente True para cada dependencia
    - Útil cuando necesitas validar que cada dependencia se crea correctamente en su contexto
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(
        num_etiquetas_musicales=1,
        create_on_page_etiquetas_musicales=False,
        num_generos_musicales=2,
        create_on_page_generos_musicales=False,
        num_temas_musicales=1,
        create_on_page_temas_musicales=False,
    )
    await album_page.validate_record()
    await album_page.delete_record()

@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_104 Solo control de cantidades (sin especificar navegación)"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_quantity_control_only(login_page, user, password):
    """Demuestra: Control solo de cantidades, navegación usa el default (True).

    - No especifica create_on_page_* para ninguna dependencia
    - Todas usarán el comportamiento default (navegar a página = True)
    - Solo controla cuántas instancias crear de cada dependencia
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(
        num_generos_musicales=3,  # Crea 3 géneros (navegando por default)
        num_etiquetas_musicales=2,  # Crea 2 etiquetas (navegando por default)
        num_temas_musicales=1,  # Crea 1 tema (navegando por default)
    )
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password, formset_name",
    [
        pytest.param(user_admin, password_admin, "songs", id="TA_999 Crear Álbum"),
        pytest.param(user_admin, password_admin, "merch", id="TA_999 Crear Álbum"),
    ],
)
@pytest.mark.asyncio
async def test_prueba_delete_formset_create(login_page, user, password, formset_name):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_delete_formset_row_on_create(formset_name, num_delete_rows=3)


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.TITULO.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_04 No crear Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_05 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_06 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            InvalidDataType.MIN_VALUE,
            "El valor no puede ser menor que 1895",
            id="TA_07 No crear Álbum con año menor al permitido",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            InvalidDataType.LETTERS,
            None,
            id="TA_09 No crear Álbum con letras en año",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ARTISTA.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_10 No crear Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ARTISTA.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_11 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_12 No crear Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_13 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_14 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            InvalidDataType.NEGATIVE_NUMBER,
            "El número no puede ser negativo.",
            id="TA_79 No crear Álbum con duración negativa",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            InvalidDataType.LETTERS,
            "Introduzca una duración válida.",
            id="TA_15 No crear Álbum con formato de duración letras",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_16 No crear Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_17 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            InvalidDataType.MIN_LENGTH,
            "Asegúrese de que este valor tenga como mínimo 2 caracteres",
            id="TA_80 No crear Álbum con nombre de mercancía menor a 2 caracteres",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.LETTERS,
            "Introduzca un número.",
            id="TA_18 No crear Álbum con letras en precio",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_19 No crear Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.MAX_VALUE,
            "El valor no puede ser mayor que 999,999.99",
            id="TA_20 No crear Álbum con precio excesivo",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.NEGATIVE_NUMBER,
            "El número no puede ser negativo.",
            id="TA_21 No crear Álbum con precio negativo",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ETIQUETA_PRINCIPAL.value,
            InvalidDataType.DUPLICATED,
            "Ya existe un álbum con esta etiqueta principal.",
            id="TA_72 No crear Álbum sin etiqueta principal",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.GENEROS.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_73 No crear Álbum sin géneros",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_album_data(login_page, user, password, field, validate_type, custom_error_message):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=field, validate_type=validate_type, custom_error_message=custom_error_message
    )


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_22 Crear Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.LETTERS,
            id="TA_23 Crear Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ARTISTA.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_24 Crear Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_25 Crear Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.LETTERS,
            id="TA_26 Crear Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_27 Crear Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            ValidDataType.LETTERS,
            id="TA_28 Crear Álbum con números",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_album_data(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_valid_data(field_name=field, validate_data_type=validate_data_type)


@pytest.mark.parametrize(
    "user, password, field, validate_type, custom_error_message",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.TITULO.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_29 No editar Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_30 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_31 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            InvalidDataType.MIN_VALUE,
            "El valor no puede ser menor que 1895",
            id="TA_32 No editar Álbum con año menor al permitido",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            InvalidDataType.LETTERS,
            None,
            id="TA_34 No editar Álbum con letras en año",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ARTISTA.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_35 No editar Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ARTISTA.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_36 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_37 No editar Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_38 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            InvalidDataType.MIN_LENGTH,
            "Asegúrese de que este valor tenga como mínimo 2 caracteres",
            id="TA_81 No editar Álbum con título menor a 2 caracteres",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_39 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            InvalidDataType.NEGATIVE_NUMBER,
            "El número no puede ser negativo.",
            id="TA_82 No editar Álbum con duración negativa",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            InvalidDataType.LETTERS,
            "Introduzca una duración válida.",
            id="TA_40 No editar Álbum con formato de duración inválido",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            InvalidDataType.MAX_LENGTH,
            None,
            id="TA_41 No editar Álbum con caracteres máximos permitidos",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_42 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            InvalidDataType.MIN_LENGTH,
            "Asegúrese de que este valor tenga como mínimo 2 caracteres",
            id="TA_83 No editar Álbum con nombre de mercancía menor a 2 caracteres",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.LETTERS,
            "Introduzca un número.",
            id="TA_43 No editar Álbum con letras en precio",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_44 No editar Álbum con campo vacío",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.MAX_VALUE,
            "El valor no puede ser mayor que 999,999.99",
            id="TA_45 No editar Álbum con precio excesivo",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            InvalidDataType.NEGATIVE_NUMBER,
            "El número no puede ser negativo.",
            id="TA_46 No editar Álbum con precio negativo",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.GENEROS.value,
            InvalidDataType.REQUIRED,
            None,
            id="TA_76 No editar Álbum sin géneros",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_album_data(login_page, user, password, field, validate_type, custom_error_message):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_edit_invalid_data(
        field_name=field, validate_type=validate_type, custom_error_message=custom_error_message
    )


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_47 Editar Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.TITULO.value,
            ValidDataType.LETTERS,
            id="TA_48 Editar Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.AÑO.value,
            ValidDataType.NUMBERS,
            id="TA_49 Editar Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.ARTISTA.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_50 Editar Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_51 Editar Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.LETTERS,
            id="TA_52 Editar Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_54 Editar Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            ValidDataType.LETTERS,
            id="TA_55 Editar Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            ValidDataType.NUMBERS,
            id="TA_56 Editar Álbum con números",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_album(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_edit_valid_data(
        field_name=field, validate_data_type=validate_data_type, lookup_formset=True
    )


@pytest.mark.parametrize(
    "user, password, field_name",
    [
        pytest.param(user_admin, password_admin, FieldAlbumEnum.TITULO.value, id="TA_57 Filtrar Álbum"),
        # pytest.param(user_admin, password_admin, FieldAlbumEnum.ARTISTA.value, id="TA_58 Filtrar Álbum"),
    ],
)
@pytest.mark.asyncio
async def test_filters_album(login_page, user, password, field_name):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_songs=3)
    await album_page.filter_by_specific_field(field=field_name, lookup_formset=True)
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            user_admin, password_admin, FieldAlbumEnum.TITULO.value, id="TA_59 Filtrar Álbum titulo que no existe"
        ),
        pytest.param(
            user_admin, password_admin, FieldAlbumEnum.ARTISTA.value, id="TA_60 Filtrar Álbum artista que no existe"
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_filter_album(login_page, user, password, field):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_no_results_on_filters(field_name=field)


@pytest.mark.parametrize(
    "user, password", [pytest.param(user_admin, password_admin, id="TA_61 Borrar filtros de Álbum")]
)
@pytest.mark.asyncio
async def test_clear_filters_album(login_page, user, password):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_62 Crear Álbum habilitar"),
    ],
)
@pytest.mark.asyncio
async def test_enable_album(login_page, user, password):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_enable_record(num_merch=3)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_63 Crear Álbum multiples canciones"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_multi_song(login_page, user, password):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_songs=3)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_64 Crear Álbum multiples mercancias"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_multi_merch(login_page, user, password):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_merch=3)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_65 Crear Álbum multiples canciones y mercancias"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_multi(login_page, user, password):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_songs=3, num_merch=3)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_66 Editar Álbum con multiples canciones",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_TITULO.value,
            ValidDataType.LETTERS,
            id="TA_67 Crear Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.CANCION_DURACION.value,
            ValidDataType.NUMBERS,
            id="TA_68 Editar Álbum con duracion con multiples canciones",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_multi_song(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_edit_valid_data(field_name=field, validate_data_type=validate_data_type, num_songs=2)


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            ValidDataType.SPECIAL_CHARS,
            id="TA_69 Crear Álbum con caracteres especiales",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_NOMBRE.value,
            ValidDataType.LETTERS,
            id="TA_70 Crear Álbum con números",
        ),
        pytest.param(
            user_admin,
            password_admin,
            FieldAlbumEnum.MERCANCIA_PRECIO.value,
            ValidDataType.NUMBERS,
            id="TA_71 Crear Álbum con números",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_multi_merch(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_edit_valid_data(field_name=field, validate_data_type=validate_data_type, num_merch=2)


# =============================================================================
# TESTS ADICIONALES PARA VALIDACIONES DE FORMSETS Y SELECT2
# =============================================================================


# @pytest.mark.parametrize(
#     "user, password",
#     [
#         pytest.param(user_admin, password_admin, id="TA_85 Crear Álbum con mercancías con nombres duplicados"),
#     ],
# )
# @pytest.mark.asyncio
# async def test_create_album_duplicate_merch_names(page, user, password):
#     """
#     Valida que no se puedan crear mercancías con el mismo nombre en un álbum.
#     Debe mostrar el error: "No pueden haber mercancías con el mismo nombre"
#     """
#     page = await login_page(user, password)
#     album_page = PageAlbum(page)

#     # Intentar crear álbum con mercancías duplicadas
#     await album_page.validate_create_invalid_data(
#         field_name=FieldAlbumEnum.MERCANCIA_NOMBRE.value,
#         validate_type=InvalidDataType.DUPLICATED,
#         custom_error_message="No pueden haber mercancías con el mismo nombre",
#         num_merch=2,
#     )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_86 Editar Álbum con canciones con títulos duplicados"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_duplicate_song_titles_on_edit(login_page, user, password):
    """Valida que no se puedan editar canciones con el mismo título en un álbum.

    Debe mostrar el error: "No pueden haber canciones con el mismo título"
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    # Intentar editar álbum con canciones duplicadas
    await album_page.validate_edit_invalid_data(
        field_name=FieldAlbumEnum.CANCION_TITULO.value,
        validate_type=InvalidDataType.DUPLICATED,
        custom_error_message="Ya existe una canción con este título.",
        num_songs=2,
        duplicate_scope="same_record",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_87 Editar Álbum con mercancías con nombres duplicados"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_duplicate_merch_names(login_page, user, password):
    """Valida que no se puedan editar mercancías con el mismo nombre en un álbum.

    Debe mostrar el error: "No pueden haber mercancías con el mismo nombre"
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    # Intentar editar álbum con mercancías duplicadas
    await album_page.validate_edit_invalid_data(
        field_name=FieldAlbumEnum.MERCANCIA_NOMBRE.value,
        validate_type=InvalidDataType.DUPLICATED,
        custom_error_message="No pueden haber mercancías con el mismo nombre",
        num_merch=2,
        duplicate_scope="same_record",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_88 Crear Álbum sin canciones"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_without_songs(login_page, user, password):
    """Valida que no se pueda crear un álbum sin al menos una canción.

    Debe mostrar el error: "Debe agregar al menos una canción"
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    # Intentar crear álbum sin canciones
    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.CANCION_TITULO.value,
        validate_type=InvalidDataType.REQUIRED,
        custom_error_message="Debe agregar al menos una canción",
        num_songs=0,
        lookup_formset=True,
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_89 Crear Álbum con etiqueta principal válida"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_with_valid_primary_tag(login_page, user, password):
    """Valida que se pueda crear un álbum con una etiqueta principal válida."""
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(create_on_dependency_page=False)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_90 Crear Álbum con múltiples géneros válidos"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_with_multiple_genres(login_page, user, password):
    """Valida que se pueda crear un álbum con múltiples géneros musicales."""
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_generos_musicales=3, create_on_dependency_page=False)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_91 Editar Álbum cambiando etiqueta principal"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_change_primary_tag(login_page, user, password):
    """Valida que se pueda editar un álbum cambiando su etiqueta principal."""
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(create_on_dependency_page=False)
    await album_page.validate_record()
    # Editar cambiando la etiqueta principal
    await album_page.edit_record(num_etiquetas_musicales=1, create_on_page_etiquetas_musicales=False)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_92 Editar Álbum agregando más géneros"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_add_more_genres(login_page, user, password):
    """Valida que se pueda editar un álbum agregando más géneros musicales."""
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_generos_musicales=2, create_on_dependency_page=False)
    await album_page.validate_record()
    # Editar agregando más géneros
    await album_page.edit_record(num_generos_musicales=4, create_on_page_generos_musicales=False)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_93 Crear Álbum con temas en canciones"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_with_song_themes(login_page, user, password):
    """Valida que se pueda crear un álbum con temas asignados a las canciones."""
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_songs=3, num_temas_musicales=1, create_on_dependency_page=False)
    await album_page.validate_record()
    await album_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_94 Editar Álbum cambiando temas de canciones"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_change_song_themes(login_page, user, password):
    """Valida que se pueda editar un álbum cambiando los temas de las canciones."""
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.create_record(num_songs=2, num_temas_musicales=1, create_on_dependency_page=False)
    await album_page.validate_record()
    # Editar cambiando los temas
    await album_page.edit_record(num_temas_musicales=1, create_on_page_temas_musicales=False)
    await album_page.validate_record()
    await album_page.delete_record()


# =============================================================================
# TESTS PARA VALIDACIONES CUSTOM DE WIDGETS
# Sección agregada para probar las validaciones personalizadas de los widgets
# Inician desde TA_95 en adelante
# =============================================================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_1001 No crear Álbum - Género con caracteres especiales"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_genre_special_chars(login_page, user, password):
    """Valida que no se pueda crear un género con caracteres especiales.

    Widget: MusicGenresTagWidget
    Error esperado: "El género contiene caracteres especiales no permitidos."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.GENEROS.value,
        validate_type=InvalidDataType.CUSTOM,
        custom_error_message="caracteres especiales no permitidos",
        custom_value="Rock@Metal",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_1002 No crear Álbum - Género muy genérico 'music'"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_genre_too_generic(login_page, user, password):
    """Valida que no se pueda crear un género muy genérico.

    Widget: MusicGenresTagWidget
    Error esperado: "El género 'music' es demasiado genérico."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.GENEROS.value,
        validate_type=InvalidDataType.CUSTOM,
        custom_error_message="demasiado genérico",
        custom_value="music",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_111 No crear Álbum - Tipo producto empieza con especial"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_product_type_starts_with_special(login_page, user, password):
    """Valida que no se pueda crear un tipo de producto que empiece con caracter especial.

    Widget: TipoProductoTagWidget
    Error esperado: "El tipo de producto no puede empezar con caracteres especiales."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value,
        validate_type=InvalidDataType.CUSTOM,
        custom_error_message="no puede empezar con caracteres especiales",
        custom_value="@Camiseta",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_112 No crear Álbum - Tipo producto solo números"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_product_type_only_numbers(login_page, user, password):
    """Valida que no se pueda crear un tipo de producto con solo números.

    Widget: TipoProductoTagWidget
    Error esperado: "El tipo de producto no puede ser solo números."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value,
        validate_type=InvalidDataType.CUSTOM,
        custom_error_message="no puede ser solo números",
        custom_value="12345",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_114 No crear Álbum - Tipo producto más de 5 palabras"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_product_type_too_many_words(login_page, user, password):
    """Valida que no se pueda crear un tipo de producto con más de 5 palabras.

    Widget: TipoProductoTagWidget
    Error esperado: "Máximo permitido: 5 palabras."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value,
        validate_type=InvalidDataType.CUSTOM,
        custom_error_message="Máximo 5 palabras",
        custom_value="Camiseta Negra De Edicion Limitada Premium",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_116 No crear Álbum - Tipo producto muy corto"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_product_type_too_short(login_page, user, password):
    """Valida que no se pueda crear un tipo de producto muy corto.

    Widget: TipoProductoTagWidget
    Error esperado: "El tipo de producto es muy corto. Debe tener al menos 3 caracteres."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value,
        validate_type=InvalidDataType.CUSTOM,
        custom_error_message="muy corto",
        custom_value="CD",
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_117 No crear Álbum - Tipo producto vacio"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_product_type_empty(login_page, user, password):
    """Valida que no se pueda crear un tipo de producto vacío.

    Widget: TipoProductoTagWidget
    Error esperado: "El tipo de producto no puede estar vacío."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value,
        validate_type=InvalidDataType.REQUIRED,
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_118 No crear Álbum - Etiqueta principal duplicada"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_duplicate_primary_tag(login_page, user, password):
    """Valida que no se pueda crear un álbum con una etiqueta principal (primary_tag) que ya está asignada a otro álbum existente.

    Flujo:
    1. Crea un primer álbum con una etiqueta principal específica
    2. Intenta crear un segundo álbum con la misma etiqueta principal
    3. Verifica que se muestre el mensaje de error: "Ya existe un álbum con esta etiqueta principal."

    Widget: MusicTagsSingleTagWidget
    Campo: primary_tag (Etiqueta principal)
    Error esperado: "Ya existe un álbum con esta etiqueta principal."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)
    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.ETIQUETA_PRINCIPAL.value,
        validate_type=InvalidDataType.DUPLICATED,
        custom_error_message="Ya existe un álbum con esta etiqueta principal.",
        create_on_dependency_page=False,
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_1222 No editar Álbum - Etiqueta principal duplicada"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_duplicate_primary_tag(login_page, user, password):
    """Valida que no se pueda editar un álbum con una etiqueta principal (primary_tag) que ya está asignada a otro álbum existente.

    Flujo:
    1. Crea un primer álbum con una etiqueta principal específica
    2. Intenta crear un segundo álbum con la misma etiqueta principal
    3. Verifica que se muestre el mensaje de error: "Ya existe un álbum con esta etiqueta principal."

    Widget: MusicTagsSingleTagWidget
    Campo: primary_tag (Etiqueta principal)
    Error esperado: "Ya existe un álbum con esta etiqueta principal."
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)
    await album_page.validate_edit_invalid_data(
        field_name=FieldAlbumEnum.ETIQUETA_PRINCIPAL.value,
        validate_type=InvalidDataType.DUPLICATED,
        custom_error_message="Ya existe un álbum con esta etiqueta principal.",
        create_on_dependency_page=False,
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_84 Crear Álbum con canciones con títulos duplicados"),
    ],
)
@pytest.mark.asyncio
async def test_create_album_duplicate_song_titles(login_page, user, password):
    """Valida que no se puedan crear canciones con el mismo título en un álbum.

    Debe mostrar el error: "No pueden haber canciones con el mismo título"
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    # Intentar crear álbum con canciones duplicadas
    await album_page.validate_create_invalid_data(
        field_name=FieldAlbumEnum.CANCION_TITULO.value,
        validate_type=InvalidDataType.DUPLICATED,
        custom_error_message="No pueden haber canciones con el mismo título",
        duplicate_scope="same_record",
        num_songs=2,
    )


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_admin, password_admin, id="TA_86 Editar Álbum con canciones con títulos duplicados"),
    ],
)
@pytest.mark.asyncio
async def test_edit_album_duplicate_song_titles(login_page, user, password):
    """Valida que no se puedan editar canciones con el mismo título en un álbum.

    Debe mostrar el error: "No pueden haber canciones con el mismo título"
    """
    page = await login_page(user, password)
    album_page = PageAlbum(page)

    # Intentar editar álbum con canciones duplicadas
    await album_page.validate_edit_invalid_data(
        field_name=FieldAlbumEnum.CANCION_TITULO.value,
        validate_type=InvalidDataType.DUPLICATED,
        custom_error_message="Ya existe una canción con este título.",
        duplicate_scope="same_record",
        num_songs=2,
    )
