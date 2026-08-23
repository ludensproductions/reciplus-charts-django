import pytest
from tests.pages.core.constants import InvalidDataType, ValidDataType
from pages.catalogos.page_evidencia import FieldEvidenciaEnum, PageEvidencia

from utils.user_constants import PASSWORD_ADMIN, USER_ADMIN


INVALID_FILE_ERROR_MESSAGE = "Las extensiones permitidas son:"


async def _validate_invalid_file_format_create(login_page, user, password, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_create_invalid_data(
        field, InvalidDataType.INVALID_FORMAT, INVALID_FILE_ERROR_MESSAGE
    )


async def _validate_invalid_file_format_edit(login_page, user, password, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_edit_invalid_data(field, InvalidDataType.INVALID_FORMAT, INVALID_FILE_ERROR_MESSAGE)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EVI_01 Crear, validar y eliminar Evidencia",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_evidencia(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.create_record(validate_record=True)
    await evidencia_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            id="EVI_02 Editar y validar Evidencia",
        ),
    ],
)
@pytest.mark.asyncio
async def test_edit_evidencia(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.create_record()
    await evidencia_page.edit_record(validate_record=True)
    await evidencia_page.delete_record()


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_03 No crear con caracteres máximos en nombre de caso",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_04 No crear con nombre de caso vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_evidencia_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_create_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.MAX_LENGTH,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_05 No editar con caracteres máximos en nombre de caso",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            InvalidDataType.REQUIRED,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_06 No editar con nombre de caso vacío",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_edit_evidencia_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_edit_invalid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_07 Crear con caracteres especiales en nombre de caso",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_08 Crear con solo letras en nombre de caso",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_evidencia_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_create_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_09 Cancelar formulario de creación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_create_form(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_cancel_create_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_10 Filtrar por nombre de caso",
        ),
    ],
)
@pytest.mark.asyncio
async def test_filter_by_field(login_page, user, password, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.create_record()
    await evidencia_page.filter_by_specific_field(field)
    await evidencia_page.delete_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_11 Filtros sin resultados"),
    ],
)
@pytest.mark.asyncio
async def test_no_results_on_filters(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_no_results_on_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_12 Limpiar filtros"),
    ],
)
@pytest.mark.asyncio
async def test_clear_filters(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_clear_filters_button()


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_24 No crear con formato inválido en archivo TXT")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_text_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.TEXT_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_25 No crear con formato inválido en archivo CSV")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_csv_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.CSV_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_26 No crear con formato inválido en archivo LOG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_log_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.LOG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_27 No crear con formato inválido en archivo PDF")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_pdf_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.PDF_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_28 No crear con formato inválido en archivo DOC")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_doc_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.DOC_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_29 No crear con formato inválido en archivo DOCX")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_docx_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.DOCX_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_30 No crear con formato inválido en archivo ODT")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_odt_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.ODT_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_31 No crear con formato inválido en archivo XLS")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_xls_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.XLS_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_32 No crear con formato inválido en archivo XLSX")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_xlsx_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.XLSX_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_33 No crear con formato inválido en archivo ODS")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_ods_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.ODS_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_34 No crear con formato inválido en archivo PPT")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_ppt_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.PPT_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_35 No crear con formato inválido en archivo PPTX")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_pptx_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.PPTX_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_36 No crear con formato inválido en archivo ODP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_odp_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.ODP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_37 No crear con formato inválido en archivo JPG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_jpg_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.JPG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_38 No crear con formato inválido en archivo JPEG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_jpeg_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.JPEG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_39 No crear con formato inválido en archivo PNG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_png_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.PNG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_40 No crear con formato inválido en archivo GIF")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_gif_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.GIF_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_41 No crear con formato inválido en archivo BMP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_bmp_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.BMP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_42 No crear con formato inválido en archivo WEBP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_webp_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.WEBP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_43 No crear con formato inválido en archivo ZIP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_zip_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.ZIP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_44 No crear con formato inválido en archivo RAR")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_rar_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.RAR_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_45 No crear con formato inválido en archivo 7Z")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_sevenzip_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.SEVENZIP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_46 No crear con formato inválido en archivo misceláneo")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_create_misc_file(login_page, user, password):
    await _validate_invalid_file_format_create(login_page, user, password, FieldEvidenciaEnum.MISC.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_47 No editar con formato inválido en archivo TXT")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_text_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.TEXT_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_48 No editar con formato inválido en archivo CSV")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_csv_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.CSV_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_49 No editar con formato inválido en archivo LOG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_log_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.LOG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_50 No editar con formato inválido en archivo PDF")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_pdf_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.PDF_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_51 No editar con formato inválido en archivo DOC")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_doc_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.DOC_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_52 No editar con formato inválido en archivo DOCX")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_docx_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.DOCX_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_53 No editar con formato inválido en archivo ODT")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_odt_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.ODT_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_54 No editar con formato inválido en archivo XLS")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_xls_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.XLS_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_55 No editar con formato inválido en archivo XLSX")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_xlsx_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.XLSX_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_56 No editar con formato inválido en archivo ODS")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_ods_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.ODS_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_57 No editar con formato inválido en archivo PPT")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_ppt_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.PPT_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_58 No editar con formato inválido en archivo PPTX")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_pptx_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.PPTX_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_59 No editar con formato inválido en archivo ODP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_odp_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.ODP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_60 No editar con formato inválido en archivo JPG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_jpg_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.JPG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_61 No editar con formato inválido en archivo JPEG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_jpeg_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.JPEG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_62 No editar con formato inválido en archivo PNG")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_png_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.PNG_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_63 No editar con formato inválido en archivo GIF")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_gif_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.GIF_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_64 No editar con formato inválido en archivo BMP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_bmp_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.BMP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_65 No editar con formato inválido en archivo WEBP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_webp_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.WEBP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_66 No editar con formato inválido en archivo ZIP")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_zip_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.ZIP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_67 No editar con formato inválido en archivo RAR")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_rar_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.RAR_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_68 No editar con formato inválido en archivo 7Z")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_sevenzip_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.SEVENZIP_FILE.value)


@pytest.mark.parametrize(
    "user, password",
    [pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_69 No editar con formato inválido en archivo misceláneo")],
)
@pytest.mark.asyncio
async def test_invalid_file_format_edit_misc_file(login_page, user, password):
    await _validate_invalid_file_format_edit(login_page, user, password, FieldEvidenciaEnum.MISC.value)


@pytest.mark.parametrize(
    "user, password, validate_type, field",
    [
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.SPECIAL_CHARS,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_13 Editar con caracteres especiales en nombre de caso",
        ),
        pytest.param(
            USER_ADMIN,
            PASSWORD_ADMIN,
            ValidDataType.LETTERS,
            FieldEvidenciaEnum.CASE_NAME.value,
            id="EVI_14 Editar con solo letras en nombre de caso",
        ),
    ],
)
@pytest.mark.asyncio
async def test_valid_edit_evidencia_data(login_page, user, password, validate_type, field):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_edit_valid_data(field, validate_type)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_15 Habilitar evidencia"),
    ],
)
@pytest.mark.asyncio
async def test_enable_evidencia(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_enable_record()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_16 Cancelar formulario de edición"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_edit_form(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_cancel_edit_form_returns_to_index()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_17 Botón volver en creación"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_create(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_back_button_on_create()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_18 Botón volver en edición"),
    ],
)
@pytest.mark.asyncio
async def test_back_button_on_edit(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_back_button_on_edit()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_19 Editar sin cambios"),
    ],
)
@pytest.mark.asyncio
async def test_edit_without_changes(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_edit_without_changes()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_20 Cancelar modal de eliminación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_delete_modal(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_cancel_delete_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_21 Cancelar modal de habilitación"),
    ],
)
@pytest.mark.asyncio
async def test_cancel_enable_modal(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_cancel_enable_modal()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_22 Filtros vacíos"),
    ],
)
@pytest.mark.asyncio
async def test_empty_filters(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.validate_empty_filters()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVI_23 Smoke CRUD evidencia"),
    ],
)
@pytest.mark.asyncio
async def test_smoke_evidencia(login_page, user, password):
    page = await login_page(user, password)
    evidencia_page = PageEvidencia(page)
    await evidencia_page.create_record()
    await evidencia_page.validate_record()
    await evidencia_page.edit_record()
    await evidencia_page.validate_record()
    await evidencia_page.delete_record()
