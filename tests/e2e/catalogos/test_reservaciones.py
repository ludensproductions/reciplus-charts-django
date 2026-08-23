import pytest
from datetime import datetime, timedelta
from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN
from pages.catalogos.page_reservacion import FieldReservacionesEnum, PageReservacion
from datetime import datetime, timedelta
from pages.core.constants import InvalidDataType, ValidDataType
from utils.utils_functions import format_date_in_dd_mm_aaaa, generate_random_int, generate_random_string

# # ================================
# # TESTS BÁSICOS CRUD COMPLETOS
# # ================================


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_01 CRUD completo reservación"),
    ],
)
@pytest.mark.asyncio
async def test_complete_crud_operations(login_page, user, password):
    """Test completo de todas las operaciones CRUD."""
    page = await login_page(user, password)
    reservaciones = PageReservacion(page)

    # Generar fecha de mañana para el campo Fecha y hora de llegada
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime("%Y-%m-%dT%H:%M")

    # Crear, ver detalle, editar, ver detalle nuevamente, eliminar
    await reservaciones.create_record(
        **{FieldReservacionesEnum.FECHA_HORA_LLEGADA.value: tomorrow_formatted}
    )
    await reservaciones.validate_record()
    await reservaciones.edit_record()
    await reservaciones.validate_record()
    await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [
#         pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_02 Crear solo campos requeridos"),
#     ],
# )
# @pytest.mark.asyncio
# async def test_create_only_required_fields(login_page, user, password):
#     """Test crear reservación solo con campos obligatorios."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.create_record(only_required=True)
#     await reservaciones.validate_record()
#     await reservaciones.delete_record()


# # ================================
# # TESTS DE VALIDACIÓN - CAMPOS REQUERIDOS
# # ================================


# @pytest.mark.parametrize(
#     "user, password, field, validate_type, error_message",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             InvalidDataType.REQUIRED,
#             None,
#             id="RES_03 No crear reservación sin reservador",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_RESERVACION.value,
#             InvalidDataType.REQUIRED,
#             None,
#             id="RES_04 No crear reservación sin fecha de reservación",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_INICIO_CANCELACION.value,
#             InvalidDataType.REQUIRED,
#             None,
#             id="RES_05 No crear reservación sin fecha inicio cancelación",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_FIN_CANCELACION.value,
#             InvalidDataType.REQUIRED,
#             None,
#             id="RES_06 No crear reservación sin fecha fin cancelación",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_HORA_LLEGADA.value,
#             InvalidDataType.REQUIRED,
#             None,
#             id="RES_07 No crear reservación sin fecha y hora de llegada",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.TIPO_RESERVACION.value,
#             InvalidDataType.REQUIRED,
#             None,
#             id="RES_08 No crear reservación sin tipo de reservación",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_required_fields_validation_create(login_page, user, password, field, validate_type, error_message):
#     """Test validaciones de campos requeridos en creación."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_create_invalid_data(field, validate_type, error_message)


# @pytest.mark.parametrize(
#     "user, password, field, validate_type",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             InvalidDataType.REQUIRED,
#             id="RES_09 No editar reservación eliminando reservador",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_RESERVACION.value,
#             InvalidDataType.REQUIRED,
#             id="RES_10 No editar reservación eliminando fecha de reservación",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_HORA_LLEGADA.value,
#             InvalidDataType.REQUIRED,
#             id="RES_11 No editar reservación eliminando fecha y hora de llegada",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_required_fields_validation_edit(login_page, user, password, field, validate_type):
#     """Test validaciones de campos requeridos en edición."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_edit_invalid_data(field, validate_type)


# # ================================
# # TESTS DE VALIDACIÓN - LONGITUD MÁXIMA
# # ================================


# @pytest.mark.parametrize(
#     "user, password, field, validate_type",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             InvalidDataType.MAX_LENGTH,
#             id="RES_12 No crear reservación con reservador muy largo (>100)",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_max_length_validation(login_page, user, password, field, validate_type):
#     """Test validaciones de longitud máxima."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_create_invalid_data(field, validate_type)


# # ================================
# # TESTS DE VALIDACIÓN - VALORES MÍNIMOS/MÁXIMOS
# # ================================


# @pytest.mark.parametrize(
#     "user, password, field, validate_type, error_message",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.CARGO_EXTRA.value,
#             InvalidDataType.MIN_VALUE,
#             "Asegúrese de que este valor sea mayor o igual a 0.",
#             id="RES_13 No crear reservación con cargo extra negativo",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.PUNTOS_PROMOCION.value,
#             InvalidDataType.MIN_VALUE,
#             "Asegúrese de que este valor sea mayor o igual a 0.",
#             id="RES_14 No crear reservación con puntos promoción negativos",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_min_value_validation(login_page, user, password, field, validate_type, error_message):
#     """Test validaciones de valor mínimo."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_create_invalid_data(field, validate_type, error_message)


# # ================================
# # TESTS DE VALIDACIÓN - RANGO DE FECHAS
# # ================================


# @pytest.mark.parametrize(
#     "user, password, field, validate_type, error_message",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.FECHA_INICIO_CANCELACION.value,
#             InvalidDataType.RANGE_OF_DATES,
#             "La fecha de inicio no puede ser posterior a la fecha de fin.",
#             id="RES_15 No crear reservación con rango fechas cancelación inválido",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_invalid_date_range_validation(login_page, user, password, field, validate_type, error_message):
#     """Test validación de rango de fechas de cancelación inválido."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_create_invalid_data(field, validate_type, error_message)


# # ================================
# # TESTS DE VALIDACIÓN - DATOS VÁLIDOS
# # ================================


# @pytest.mark.parametrize(
#     "user, password, field, validate_data_type",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             ValidDataType.SPECIAL_CHARS,
#             id="RES_16 Crear reservación con reservador con caracteres especiales",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             ValidDataType.NUMBERS,
#             id="RES_17 Crear reservación con reservador con números",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             ValidDataType.LETTERS,
#             id="RES_18 Crear reservación con reservador solo letras",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.CARGO_EXTRA.value,
#             ValidDataType.DECIMAL,
#             id="RES_19 Crear reservación con cargo extra decimal",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.PUNTOS_PROMOCION.value,
#             ValidDataType.NUMBERS,
#             id="RES_20 Crear reservación con puntos promoción números",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_valid_data_creation(login_page, user, password, field, validate_data_type):
#     """Test creación con datos válidos."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_create_valid_data(field, validate_data_type)


# @pytest.mark.parametrize(
#     "user, password, field, validate_data_type",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             ValidDataType.SPECIAL_CHARS,
#             id="RES_21 Editar reservación con reservador con caracteres especiales",
#         ),
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             ValidDataType.LETTERS,
#             id="RES_22 Editar reservación con reservador solo letras",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_valid_data_editing(login_page, user, password, field, validate_data_type):
#     """Test edición con datos válidos."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.validate_edit_valid_data(field, validate_data_type)


# # ================================
# # TESTS DE FILTRADO
# # ================================


# @pytest.mark.parametrize(
#     "user, password, field",
#     [
#         pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.RESERVADOR.value, id="RES_23 Filtrar por reservador"),
#         pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.FECHA_RESERVACION.value, id="RES_24 Filtrar por fecha reservación"),
#         pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.FECHA_INICIO_CANCELACION.value, id="RES_25 Filtrar por fecha inicio cancelación"),
#         pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.FECHA_FIN_CANCELACION.value, id="RES_26 Filtrar por fecha fin cancelación"),
#         pytest.param(USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.FECHA_HORA_LLEGADA.value, id="RES_27 Filtrar por fecha hora llegada"),
#     ],
# )
# @pytest.mark.asyncio
# async def test_filter_by_fields(login_page, user, password, field):
#     """Test filtrado por campos específicos."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.filter_by_specific_field(field)
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password, field",
#     [
#         pytest.param(
#             USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.FECHA_INICIO_CANCELACION.value, id="RES_28 Filtrar por fecha inicio cancelación específica"
#         ),
#         pytest.param(
#             USER_ADMIN, PASSWORD_ADMIN, FieldReservacionesEnum.FECHA_FIN_CANCELACION.value, id="RES_29 Filtrar por fecha fin cancelación específica"
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_filter_by_date(login_page, user, password, field):
#     """Test filtrado por fechas específicas."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)

#     future_date = datetime.now() + timedelta(days=generate_random_int(1, 10))
#     await reservaciones.create_record(
#         validate_record=False,
#         **{field: format_date_in_dd_mm_aaaa(future_date)},
#     )
#     await reservaciones.filter_by_specific_field(field)
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password, field",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             id="RES_30 Validar sin resultados filtro por reservador inexistente",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_no_results_filter_by_field(login_page, user, password, field):
#     """Test comportamiento cuando no hay resultados para campos de tipo input text."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_no_results_on_filters(field_name=field)


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_31 Validar sin resultados filtro general")],
# )
# @pytest.mark.asyncio
# async def test_no_results_filter(login_page, user, password):
#     """Test comportamiento cuando no hay resultados para filtros generales."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_no_results_on_filters()


# # ================================
# # TESTS DE VALIDACIÓN DE BOTONES Y NAVEGACIÓN
# # ================================


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_32 Validar botón cancelar en crear")],
# )
# @pytest.mark.asyncio
# async def test_validate_cancel_create_form(login_page, user, password):
#     """Test validar que el botón cancelar en crear funcione correctamente."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_cancel_create_form_returns_to_index()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_33 Validar botón cancelar en editar")],
# )
# @pytest.mark.asyncio
# async def test_validate_cancel_edit_form(login_page, user, password):
#     """Test validar que el botón cancelar en editar funcione correctamente."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_cancel_edit_form_returns_to_index()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_34 Validar botón atrás en crear")],
# )
# @pytest.mark.asyncio
# async def test_validate_back_button_create(login_page, user, password):
#     """Test validar que el botón atrás en crear funcione correctamente."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_back_button_on_create()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_35 Validar botón atrás en editar")],
# )
# @pytest.mark.asyncio
# async def test_validate_back_button_edit(login_page, user, password):
#     """Test validar que el botón atrás en editar funcione correctamente."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_back_button_on_edit()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_36 Validar botón atrás en detalle")],
# )
# @pytest.mark.asyncio
# async def test_validate_back_button_detail(login_page, user, password):
#     """Test validar que el botón atrás en detalle funcione correctamente."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_back_button_on_detail()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_37 Validar botón limpiar filtros")],
# )
# @pytest.mark.asyncio
# async def test_validate_clear_filters_button(login_page, user, password):
#     """Test validar que el botón limpiar filtros funcione correctamente."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_clear_filters_button()


# # ================================
# # TESTS DE VALIDACIÓN DE MODALES
# # ================================


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_38 Validar cancelar modal eliminar")],
# )
# @pytest.mark.asyncio
# async def test_validate_cancel_delete_modal(login_page, user, password):
#     """Test validar que se pueda cancelar el modal de eliminar."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.validate_cancel_delete_modal()
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_39 Validar cancelar modal habilitar")],
# )
# @pytest.mark.asyncio
# async def test_validate_cancel_enable_modal(login_page, user, password):
#     """Test validar que se pueda cancelar el modal de habilitar."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.delete_record(validate_record=False)
#     await reservaciones.validate_cancel_enable_modal()


# @pytest.mark.parametrize(
#     "user, password, field",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             id="RES_40 Validar cancelar modal doble validación",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_validate_cancel_double_validation_modal(login_page, user, password, field):
#     """Test validar que se pueda cancelar el modal de doble validación."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_cancel_double_validation_modal(field)


# # ================================
# # TESTS DE VALIDACIÓN DE REGISTROS
# # ================================


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_41 Validar registro en detalle")],
# )
# @pytest.mark.asyncio
# async def test_validate_record_on_detail(login_page, user, password):
#     """Test validar que los datos se muestren correctamente en la página de detalle."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.validate_record_on_detail()
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_42 Validar registro en editar")],
# )
# @pytest.mark.asyncio
# async def test_validate_record_on_edit(login_page, user, password):
#     """Test validar que los datos se muestren correctamente en la página de editar."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.validate_record_on_edit()
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_43 Validar estado eliminado del registro")],
# )
# @pytest.mark.asyncio
# async def test_validate_record_deleted_state(login_page, user, password):
#     """Test validar el estado eliminado del registro."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.delete_record(validate_record=False)


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_44 Validar habilitar registro")],
# )
# @pytest.mark.asyncio
# async def test_validate_enable_record(login_page, user, password):
#     """Test validar habilitar un registro eliminado."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.delete_record(validate_record=False)
#     await reservaciones.validate_enable_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_45 Validar editar sin cambios")],
# )
# @pytest.mark.asyncio
# async def test_validate_edit_without_changes(login_page, user, password):
#     """Test validar editar un registro sin hacer cambios."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.validate_edit_without_changes()
#     await reservaciones.delete_record()


# # ================================
# # TESTS DE VALIDACIÓN DE FILTROS AVANZADOS
# # ================================


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_46 Validar filtros vacíos")],
# )
# @pytest.mark.asyncio
# async def test_validate_empty_filters(login_page, user, password):
#     """Test validar comportamiento con filtros vacíos."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_empty_filters()


# @pytest.mark.parametrize(
#     "user, password, field",
#     [
#         pytest.param(
#             USER_ADMIN,
#             PASSWORD_ADMIN,
#             FieldReservacionesEnum.RESERVADOR.value,
#             id="RES_47 Validar muchos resultados en filtro",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_validate_many_results_on_filter(login_page, user, password, field):
#     """Test validar comportamiento cuando hay muchos resultados en filtro."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.validate_many_results_on_filter(field)


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_48 Validar filtro en página actual")],
# )
# @pytest.mark.asyncio
# async def test_validate_filter_on_current_page(login_page, user, password):
#     """Test validar filtro en la página actual."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.delete_record()


# # ================================
# # TESTS DE VALIDACIÓN DE MENSAJES
# # ================================


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_49 Validar mensaje de éxito creación")],
# )
# @pytest.mark.asyncio
# async def test_validate_success_message_create(login_page, user, password):
#     """Test validar mensaje de éxito al crear."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_50 Validar mensaje de éxito edición")],
# )
# @pytest.mark.asyncio
# async def test_validate_success_message_edit(login_page, user, password):
#     """Test validar mensaje de éxito al editar."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.edit_record(validate_record=False)
#     await reservaciones.delete_record()


# @pytest.mark.parametrize(
#     "user, password",
#     [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="RES_51 Validar mensaje de éxito eliminación")],
# )
# @pytest.mark.asyncio
# async def test_validate_success_message_delete(login_page, user, password):
#     """Test validar mensaje de éxito al eliminar."""
#     page = await login_page(user, password)
#     reservaciones = PageReservacion(page)
#     await reservaciones.create_record(validate_record=False)
#     await reservaciones.delete_record(validate_record=False)
