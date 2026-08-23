import pytest
from pages.catalogos.page_evento import PageEventos, FieldEventoEnum
from tests.pages.core.constants import InvalidDataType, ValidDataType

from tests.utils.user_constants import USER_ADMIN, PASSWORD_ADMIN
from tests.utils.utils_functions import format_date_in_dd_mm_aaaa, generate_random_int
from datetime import datetime, timedelta

# ================================
# TESTS BÁSICOS CRUD COMPLETOS
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_01 CRUD completo evento"),
    ],
)
@pytest.mark.asyncio
async def test_complete_crud_operations(login_page, user, password):
    """Test completo de todas las operaciones CRUD."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Crear, ver detalle, editar, ver detalle nuevamente, eliminar
    await eventos.create_record()
    await eventos.validate_record()
    await eventos.edit_record()
    await eventos.validate_record()
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_02 Crear solo campos requeridos"),
    ],
)
@pytest.mark.asyncio
async def test_create_only_required_fields(login_page, user, password):
    """Test crear evento solo con campos obligatorios."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record(only_required=True)
    await eventos.validate_record()
    await eventos.delete_record()


# ================================
# TESTS DE VALIDACIÓN - CAMPOS REQUERIDOS
# ================================


@pytest.mark.parametrize(
    "user, password, field, validate_type, error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            InvalidDataType.REQUIRED,
            None,
            id="EVT_03 No crear evento sin título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            InvalidDataType.REQUIRED,
            None,
            id="EVT_04 No crear evento sin ubicación",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.FECHA_INICIO.value,
            InvalidDataType.REQUIRED,
            None,
            id="EVT_05 No crear evento sin fecha de inicio",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.RESPONSABLE.value,
            InvalidDataType.REQUIRED,
            None,
            id="EVT_06 No crear evento sin responsable",
        ),
    ],
)
@pytest.mark.asyncio
async def test_required_fields_validation_create(login_page, user, password, field, validate_type, error_message):
    """Test validaciones de campos requeridos en creación."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_create_invalid_data(field, validate_type, error_message)


@pytest.mark.parametrize(
    "user, password, field, validate_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            InvalidDataType.REQUIRED,
            id="EVT_07 No editar evento eliminando título",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            InvalidDataType.REQUIRED,
            id="EVT_08 No editar evento eliminando ubicación",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.FECHA_INICIO.value,
            InvalidDataType.REQUIRED,
            id="EVT_09 No editar evento eliminando fecha",
        ),
    ],
)
@pytest.mark.asyncio
async def test_required_fields_validation_edit(login_page, user, password, field, validate_type):
    """Test validaciones de campos requeridos en edición."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_edit_invalid_data(field, validate_type)


# ================================
# TESTS DE VALIDACIÓN - LONGITUD MÁXIMA
# ================================


@pytest.mark.parametrize(
    "user, password, field, validate_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            InvalidDataType.MAX_LENGTH,
            id="EVT_10 No crear evento con título muy largo (>200)",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            InvalidDataType.MAX_LENGTH,
            id="EVT_11 No crear evento con ubicación muy larga (>200)",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.CODIGO.value,
            InvalidDataType.MAX_LENGTH,
            id="EVT_12 No crear evento con código muy largo (>50)",
        ),
    ],
)
@pytest.mark.asyncio
async def test_max_length_validation(login_page, user, password, field, validate_type):
    """Test validaciones de longitud máxima."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_create_invalid_data(field, validate_type)


# ================================
# TESTS DE VALIDACIÓN - FORMSETS REQUERIDOS
# ================================


@pytest.mark.parametrize(
    "user, password, field, validate_type,error_message",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.ACTIVIDAD.value,
            InvalidDataType.REQUIRED,
            None,
            id="EVT_13 No crear evento sin actividad en formset",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.AFORO.value,
            InvalidDataType.MIN_VALUE,
            "Asegúrese de que este valor sea mayor o igual a 0.",
            id="EVT_14 No crear evento con aforo negativo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_formset_required_validation(login_page, user, password, field, validate_type, error_message):
    """Test validaciones de campos requeridos en formsets."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_create_invalid_data(field, validate_type, error_message)


# ================================
# TESTS DE VALIDACIÓN - DATOS VÁLIDOS
# ================================


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="EVT_15 Crear evento con título con caracteres especiales",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            ValidDataType.NUMBERS,
            id="EVT_16 Crear evento con título con números",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            ValidDataType.SPECIAL_CHARS,
            id="EVT_17 Crear evento con ubicación con caracteres especiales",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            ValidDataType.LETTERS,
            id="EVT_18 Crear evento con ubicación solo letras",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.CODIGO.value,
            ValidDataType.ALPHANUMERIC,
            id="EVT_19 Crear evento con código alfanumérico",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_data_creation(login_page, user, password, field, validate_data_type):
    """Test creación con datos válidos."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_create_valid_data(field, validate_data_type)


@pytest.mark.parametrize(
    "user, password, field, validate_data_type",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            ValidDataType.SPECIAL_CHARS,
            id="EVT_20 Editar evento con título con caracteres especiales",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            ValidDataType.LETTERS,
            id="EVT_21 Editar evento con ubicación solo letras",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_data_editing(login_page, user, password, field, validate_data_type):
    """Test edición con datos válidos."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_edit_valid_data(field, validate_data_type)


# ================================
# TESTS DE FILTRADO
# ================================


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldEventoEnum.TITULO.value, id="EVT_23 Filtrar por título"),
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldEventoEnum.UBICACION.value, id="EVT_24 Filtrar por ubicación"),
        pytest.param(
            USER_ADMIN, PASSWORD_ADMIN, FieldEventoEnum.RESPONSABLE.value, id="EVT_25 Filtrar por responsable"
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_fields(login_page, user, password, field):
    """Test filtrado por campos específicos."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record(validate_record=False)
    await eventos.filter_by_specific_field(field)
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN, PASSWORD_ADMIN, FieldEventoEnum.FECHA_INICIO.value, id="EVT_26 Filtrar por fecha inicio"
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_date(login_page, user, password, field):
    """Test filtrado por fechas."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    future_date = datetime.now() + timedelta(days=generate_random_int(1, 10))
    await eventos.create_record(
        validate_record=False,
        **{field: format_date_in_dd_mm_aaaa(future_date)},
    )
    await eventos.filter_by_specific_field(field)
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.TITULO.value,
            id="EVT_27 Validar sin resultados filtro por título inexistente",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.UBICACION.value,
            id="EVT_28 Validar sin resultados filtro por ubicación inexistente",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.FOLIO.value,
            id="EVT_29 Validar sin resultados filtro por folio inexistente",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.AFORO.value,
            id="EVT_30 Validar sin resultados filtro por aforo inexistente",
        ),
    ],
)
@pytest.mark.asyncio
async def test_no_results_filter_by_field(login_page, user, password, field):
    """Test comportamiento cuando no hay resultados para campos de tipo input text."""
    page = await login_page(user, password)
    eventos = PageEventos(page)
    await eventos.validate_no_results_on_filters(field_name=field)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_47 Validar sin resultados filtro por todos los campos")],
)
@pytest.mark.asyncio
async def test_no_results_filter(login_page, user, password):
    """Test comportamiento cuando no hay resultados para campos de tipo input text."""
    page = await login_page(user, password)
    eventos = PageEventos(page)
    await eventos.validate_no_results_on_filters()


# ================================
# TESTS DE FORMSETS Y MÚLTIPLES ACTIVIDADES
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_31 Crear evento con múltiples actividades"),
    ],
)
@pytest.mark.asyncio
async def test_multiple_activities_creation(login_page, user, password):
    """Test crear evento con múltiples actividades."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record(num_activities=3)
    await eventos.get_field_values()
    await eventos.get_field_values(attribute="validate_value")

    await eventos.validate_record()
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password, formset_name",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.FORMSET_ACTIVIDADES.value,
            id="EVT_32 Eliminar fila de formset en creación",
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_formset_row_create(login_page, user, password, formset_name):
    """Test eliminar fila de formset durante creación."""
    page = await login_page(user, password)
    eventos = PageEventos(page)
    await eventos.validate_delete_formset_row_on_create(formset_name, num_delete_rows=3)


@pytest.mark.parametrize(
    "user, password, formset_name",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEventoEnum.FORMSET_ACTIVIDADES.value,
            id="EVT_33 Eliminar fila de formset en edición",
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_formset_row_edit(login_page, user, password, formset_name):
    """Test eliminar fila de formset durante edición."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_delete_formset_row_on_edit(formset_name, num_delete_rows=3)


# ================================
# TESTS DE NAVEGACIÓN Y CONTROLES
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_34 Validar botón cancelar en creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    """Test botón cancelar en formulario de creación."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_35 Validar botón cancelar en edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    """Test botón cancelar en formulario de edición."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_36 Validar botones de navegación hacia atrás en crear"),
    ],
)
@pytest.mark.asyncio
async def test_back_navigation_buttons_create(login_page, user, password):
    """Test botones de navegación hacia atrás."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_37 Validar botones de navegación hacia atrás en editar"),
    ],
)
@pytest.mark.asyncio
async def test_back_navigation_buttons_edit(login_page, user, password):
    """Test botones de navegación hacia atrás."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_38 Validar botones de navegación hacia atrás en detalle"),
    ],
)
@pytest.mark.asyncio
async def test_back_navigation_buttons_detail(login_page, user, password):
    """Test botones de navegación hacia atrás."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_back_button_on_detail()


# ================================
# TESTS DE EDICIÓN SIN CAMBIOS
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_39 Editar sin realizar cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    """Test editar formulario sin realizar cambios."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_edit_without_changes()


# ================================
# TESTS DE FILTROS AVANZADOS
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_40 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    """Test limpiar filtros."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_41 Validar filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    """Test validar que filtros están vacíos."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.validate_empty_filters()


# ================================
# TESTS DE MODALES Y CONFIRMACIONES
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_42 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    """Test cancelar modal de eliminación."""
    page = await login_page(user, password)
    eventos = PageEventos(page)
    await eventos.validate_cancel_delete_modal()


# ================================
# TESTS DE OBTENCIÓN DE VALORES
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_43 Obtener valores de campos"),
    ],
)
@pytest.mark.asyncio
async def test_get_field_values(login_page, user, password):
    """Test obtener valores de campos del formulario."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record()

    field_values = await eventos.get_field_values()
    validate_values = await eventos.get_field_values(attribute="validate_value")
    filter_values = await eventos.get_field_values(attribute="filter_value")

    assert isinstance(field_values, dict)
    assert isinstance(validate_values, dict)
    assert isinstance(filter_values, dict)

    await eventos.delete_record()


# ================================
# TESTS DE SMOKE (CRÍTICOS)
# ================================


@pytest.mark.smoke
@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_44 SMOKE - Funcionalidad crítica completa"),
    ],
)
@pytest.mark.asyncio
async def test_smoke_complete_functionality(login_page, user, password):
    """Test crítico de funcionalidad completa del módulo."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Flujo crítico completo
    await eventos.create_record()
    await eventos.validate_record()
    await eventos.edit_record()
    await eventos.validate_record()
    await eventos.delete_record()


# ================================
# TESTS DE ESTRÉS Y CASOS LÍMITE
# ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_45 Crear evento con máximo de actividades"),
    ],
)
@pytest.mark.asyncio
async def test_maximum_activities(login_page, user, password):
    """Test crear evento con máximo número de actividades."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record(num_activities=5)
    await eventos.validate_record()
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_46 Evento con fecha futura lejana"),
    ],
)
@pytest.mark.asyncio
async def test_far_future_date(login_page, user, password):
    """Test crear evento con fecha muy futura."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    far_future = datetime.now() + timedelta(days=365)
    await eventos.create_record(**{FieldEventoEnum.FECHA_INICIO.value: format_date_in_dd_mm_aaaa(far_future)})
    await eventos.validate_record()
    await eventos.delete_record()


# ================================
# TESTS DE CORRECCIÓN DE BUGS EN GENERIC_PAGE
# ================================


# @pytest.mark.parametrize(
#     "user, password",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             id="EVT_47 Bug Fix: num_dependencies=0 no debe generar datos",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_bug_fix_num_dependencies_zero(login_page, user, password):
#     """Test Bug Fix #1: Cuando num_<dependency>=0, NO debe generar datos para ese campo.

#     Problema Original:
#     - Se especificaba num_actividades=0
#     - No se creaba la actividad (correcto)
#     - Pero SÍ se generaban datos para el campo actividad (incorrecto)
#     - Causaba error al intentar llenar un campo que no debería tener valor

#     Solución:
#     - Agregada validación: if num_dependencies == 0: continue
#     - Ahora NO genera datos cuando num_dependencies=0
#     """
#     page = await login_page(user, password)
#     eventos = PageEventos(page)

#     # Crear evento SIN actividades (num_activities=0)
#     await eventos.create_record(num_activities=0)
#     await eventos.validate_record()
#     await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EVT_48 Bug Fix: Formset con 1 row debe agregar 1 fila",
        ),
    ],
)
@pytest.mark.asyncio
async def test_bug_fix_formset_one_row(login_page, user, password):
    """Test Bug Fix #2: Formset con num_formset=1 debe agregar exactamente 1 fila.

    Problema Original:
    - Formset comienza con 0 rows
    - Se especifica num_activities=1
    - Se usaba range(count - 1), entonces range(0) = 0 clicks
    - NO se agregaba ninguna fila (incorrecto)

    Solución:
    - Cambiado a range(count) en lugar de range(count - 1)
    - Ahora num_activities=1 hace 1 click y agrega 1 fila correctamente
    """
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Crear evento con EXACTAMENTE 1 actividad
    await eventos.create_record(num_activities=1)
    await eventos.validate_record()
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EVT_49 Bug Fix: Formset con 2 rows debe agregar 2 filas",
        ),
    ],
)
@pytest.mark.asyncio
async def test_bug_fix_formset_two_rows(login_page, user, password):
    """Test Bug Fix #2 (caso 2): Formset con num_formset=2 debe agregar exactamente 2 filas.

    Problema Original:
    - Se especifica num_activities=2
    - Se usaba range(count - 1), entonces range(1) = 1 click
    - Solo se agregaba 1 fila en lugar de 2 (incorrecto)

    Solución:
    - Cambiado a range(count)
    - Ahora num_activities=2 hace 2 clicks y agrega 2 filas correctamente
    """
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Crear evento con EXACTAMENTE 2 actividades
    await eventos.create_record(num_activities=2)
    await eventos.validate_record()
    await eventos.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EVT_50 Bug Fix: Formset con 5 rows debe agregar 5 filas",
        ),
    ],
)
@pytest.mark.asyncio
async def test_bug_fix_formset_five_rows(login_page, user, password):
    """Test Bug Fix #2 (caso límite): Formset con num_formset=5 debe agregar exactamente 5 filas.

    Validación de que la corrección funciona con números mayores.
    """
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Crear evento con 5 actividades
    await eventos.create_record(num_activities=5)
    await eventos.validate_record()
    await eventos.delete_record()
