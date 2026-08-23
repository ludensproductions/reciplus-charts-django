from django import forms

from apps.comun.forms import AbstractModelForm

from . import consts as evidence_consts
from .models import Evidence


class EvidenceForm(AbstractModelForm):
    """Provide form fields and labels for Evidence records."""

    class Meta:
        model = Evidence
        fields = [
            "case_name",
            "text_file_evidence",
            "csv_file_evidence",
            "log_file_evidence",
            "pdf_file_evidence",
            "doc_file_evidence",
            "docx_file_evidence",
            "odt_file_evidence",
            "xls_file_evidence",
            "xlsx_file_evidence",
            "ods_file_evidence",
            "ppt_file_evidence",
            "pptx_file_evidence",
            "odp_file_evidence",
            "jpg_file_evidence",
            "jpeg_file_evidence",
            "png_file_evidence",
            "gif_file_evidence",
            "bmp_file_evidence",
            "webp_file_evidence",
            "zip_file_evidence",
            "rar_file_evidence",
            "sevenzip_file_evidence",
            "misc",
        ]

        labels = {
            "case_name": evidence_consts.CASE_NAME_LABEL,
            "text_file_evidence": evidence_consts.TEXT_FILE_EVIDENCE_FORM_LABEL,
            "csv_file_evidence": evidence_consts.CSV_FILE_EVIDENCE_FORM_LABEL,
            "log_file_evidence": evidence_consts.LOG_FILE_EVIDENCE_FORM_LABEL,
            "pdf_file_evidence": evidence_consts.PDF_FILE_EVIDENCE_FORM_LABEL,
            "doc_file_evidence": evidence_consts.DOC_FILE_EVIDENCE_FORM_LABEL,
            "docx_file_evidence": evidence_consts.DOCX_FILE_EVIDENCE_FORM_LABEL,
            "odt_file_evidence": evidence_consts.ODT_FILE_EVIDENCE_FORM_LABEL,
            "xls_file_evidence": evidence_consts.XLS_FILE_EVIDENCE_FORM_LABEL,
            "xlsx_file_evidence": evidence_consts.XLSX_FILE_EVIDENCE_FORM_LABEL,
            "ods_file_evidence": evidence_consts.ODS_FILE_EVIDENCE_FORM_LABEL,
            "ppt_file_evidence": evidence_consts.PPT_FILE_EVIDENCE_FORM_LABEL,
            "pptx_file_evidence": evidence_consts.PPTX_FILE_EVIDENCE_FORM_LABEL,
            "odp_file_evidence": evidence_consts.ODP_FILE_EVIDENCE_FORM_LABEL,
            "jpg_file_evidence": evidence_consts.JPG_FILE_EVIDENCE_FORM_LABEL,
            "jpeg_file_evidence": evidence_consts.JPEG_FILE_EVIDENCE_FORM_LABEL,
            "png_file_evidence": evidence_consts.PNG_FILE_EVIDENCE_FORM_LABEL,
            "gif_file_evidence": evidence_consts.GIF_FILE_EVIDENCE_FORM_LABEL,
            "bmp_file_evidence": evidence_consts.BMP_FILE_EVIDENCE_FORM_LABEL,
            "webp_file_evidence": evidence_consts.WEBP_FILE_EVIDENCE_FORM_LABEL,
            "zip_file_evidence": evidence_consts.ZIP_FILE_EVIDENCE_FORM_LABEL,
            "rar_file_evidence": evidence_consts.RAR_FILE_EVIDENCE_FORM_LABEL,
            "sevenzip_file_evidence": evidence_consts.SEVENZIP_FILE_EVIDENCE_FORM_LABEL,
            "misc": evidence_consts.MISC_FILE_EVIDENCE_LABEL,
        }

        widgets = {
            "case_name": forms.TextInput(attrs={"placeholder": evidence_consts.CASE_NAME_PLACEHOLDER}),
        }
