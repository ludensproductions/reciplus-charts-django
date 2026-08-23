import os
from enum import Enum

from tests.pages.core.constants import DeleteModeEnum, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldEvidenciaEnum(Enum):
    """Enum de campos para el módulo de Evidencia."""

    CASE_NAME = "case_name"
    TEXT_FILE = "text_file_evidence"
    CSV_FILE = "csv_file_evidence"
    LOG_FILE = "log_file_evidence"
    PDF_FILE = "pdf_file_evidence"
    DOC_FILE = "doc_file_evidence"
    DOCX_FILE = "docx_file_evidence"
    ODT_FILE = "odt_file_evidence"
    XLS_FILE = "xls_file_evidence"
    XLSX_FILE = "xlsx_file_evidence"
    ODS_FILE = "ods_file_evidence"
    PPT_FILE = "ppt_file_evidence"
    PPTX_FILE = "pptx_file_evidence"
    ODP_FILE = "odp_file_evidence"
    JPG_FILE = "jpg_file_evidence"
    JPEG_FILE = "jpeg_file_evidence"
    PNG_FILE = "png_file_evidence"
    GIF_FILE = "gif_file_evidence"
    BMP_FILE = "bmp_file_evidence"
    WEBP_FILE = "webp_file_evidence"
    ZIP_FILE = "zip_file_evidence"
    RAR_FILE = "rar_file_evidence"
    SEVENZIP_FILE = "sevenzip_file_evidence"
    MISC = "misc"


class PageEvidencia(GenericPage):
    """Page Object para el módulo de Evidencia."""

    def __init__(self, page):
        super().__init__(page, module_name="Evidencia", navigation=["Catálogos", "Evidencia"])
        self.delete_mode = DeleteModeEnum.TOGGLE

        self.input_field_instances = {
            FieldEvidenciaEnum.CASE_NAME.value: FieldsPage(
                page=page,
                max_length=100,
                name=FieldEvidenciaEnum.CASE_NAME.value,
            ),
            FieldEvidenciaEnum.TEXT_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.TEXT_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["txt"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.CSV_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.CSV_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["csv"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.LOG_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.LOG_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["log"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.PDF_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.PDF_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["pdf"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.DOC_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.DOC_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["doc"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.DOCX_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.DOCX_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["docx"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.ODT_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.ODT_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["odt"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.XLS_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.XLS_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["xls"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.XLSX_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.XLSX_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["xlsx"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.ODS_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.ODS_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["ods"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.PPT_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.PPT_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["ppt"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.PPTX_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.PPTX_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["pptx"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.ODP_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.ODP_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["odp"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.JPG_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.JPG_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["jpg"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.JPEG_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.JPEG_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["jpeg"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.PNG_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.PNG_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["png"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.GIF_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.GIF_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["gif"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.BMP_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.BMP_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["bmp"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.WEBP_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.WEBP_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["webp"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.ZIP_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.ZIP_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["zip"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.RAR_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.RAR_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["rar"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.SEVENZIP_FILE.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.SEVENZIP_FILE.value,
                input_type=InputType.FILE,
                allowed_values=["7z"],
                is_filter=False,
                is_indexable=False,
            ),
            FieldEvidenciaEnum.MISC.value: FieldsPage(
                page=page,
                name=FieldEvidenciaEnum.MISC.value,
                input_type=InputType.FILE,
                allowed_values=[
                    "txt",
                    "csv",
                    "log",
                    "pdf",
                    "doc",
                    "docx",
                    "odt",
                    "xls",
                    "xlsx",
                    "ods",
                    "ppt",
                    "pptx",
                    "odp",
                    "jpg",
                    "jpeg",
                    "png",
                    "gif",
                    "bmp",
                    "webp",
                    "zip",
                    "rar",
                    "7z",
                ],
                is_filter=False,
                is_indexable=False,
            ),
        }

    @staticmethod
    def _file_name_prefix(expected_file_name: str) -> str:
        """Return the filename without extension to tolerate Django storage suffixes."""
        return os.path.splitext(expected_file_name)[0]

    def _normalize_expected_file_values(self):
        """Normalize expected file values for detail/edit validations.

        Django can rename uploaded files by appending a random suffix to avoid collisions.
        Using the filename prefix keeps validation deterministic across runs.
        """
        file_fields = {
            field.title_for_validate: field
            for field in self.input_field_instances.values()
            if field.input_type == InputType.FILE
        }
        file_selectors = {
            field.field_selector: field
            for field in self.input_field_instances.values()
            if field.input_type == InputType.FILE
        }

        for validations_dict in (self.data_validate, self.edit_data_validate, self.index_data_validate):
            for key, value in list(validations_dict.items()):
                if key not in file_fields and key not in file_selectors:
                    continue
                if not isinstance(value, str):
                    continue
                validations_dict[key] = self._file_name_prefix(value)

    async def validate_record(self):
        """Validate record values including resilient file-name checks."""
        self._normalize_expected_file_values()
        await super().validate_record()
