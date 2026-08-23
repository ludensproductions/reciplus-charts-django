from django.core.validators import FileExtensionValidator
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractNullableModel
from apps.evidence import consts as evidence_consts

ALLOWED_MISC_FILE_EXTENSIONS = [
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
]


class Evidence(AbstractNullableModel):
    """Store evidence files for a case.

    This model collects evidence file uploads associated with a case name and
    allows storing multiple file types. Each field is optional unless enforced
    by validation at a higher layer.

    Attributes:
        case_name (str): Case identifier or name.
        text_file_evidence (File): TXT evidence file.
        csv_file_evidence (File): CSV evidence file.
        log_file_evidence (File): LOG evidence file.
        pdf_file_evidence (File): PDF evidence file.
        doc_file_evidence (File): DOC evidence file.
        docx_file_evidence (File): DOCX evidence file.
        odt_file_evidence (File): ODT evidence file.
        xls_file_evidence (File): XLS evidence file.
        xlsx_file_evidence (File): XLSX evidence file.
        ods_file_evidence (File): ODS evidence file.
        ppt_file_evidence (File): PPT evidence file.
        pptx_file_evidence (File): PPTX evidence file.
        odp_file_evidence (File): ODP evidence file.
        jpg_file_evidence (File): JPG evidence file.
        jpeg_file_evidence (File): JPEG evidence file.
        png_file_evidence (File): PNG evidence file.
        gif_file_evidence (File): GIF evidence file.
        bmp_file_evidence (File): BMP evidence file.
        webp_file_evidence (File): WEBP evidence file.
        zip_file_evidence (File): ZIP evidence file.
        rar_file_evidence (File): RAR evidence file.
        sevenzip_file_evidence (File): 7Z evidence file.
        misc (File): Miscellaneous evidence file.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    case_name = models.CharField(max_length=100, verbose_name=evidence_consts.CASE_NAME_LABEL)
    text_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["txt"])],
        verbose_name=evidence_consts.TEXT_FILE_EVIDENCE_LABEL,
    )
    csv_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
        verbose_name=evidence_consts.CSV_FILE_EVIDENCE_LABEL,
    )
    log_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["log"])],
        verbose_name=evidence_consts.LOG_FILE_EVIDENCE_LABEL,
    )
    pdf_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        verbose_name=evidence_consts.PDF_FILE_EVIDENCE_LABEL,
    )
    doc_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["doc"])],
        verbose_name=evidence_consts.DOC_FILE_EVIDENCE_LABEL,
    )
    docx_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["docx"])],
        verbose_name=evidence_consts.DOCX_FILE_EVIDENCE_LABEL,
    )
    odt_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["odt"])],
        verbose_name=evidence_consts.ODT_FILE_EVIDENCE_LABEL,
    )
    xls_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["xls"])],
        verbose_name=evidence_consts.XLS_FILE_EVIDENCE_LABEL,
    )
    xlsx_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"])],
        verbose_name=evidence_consts.XLSX_FILE_EVIDENCE_LABEL,
    )
    ods_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["ods"])],
        verbose_name=evidence_consts.ODS_FILE_EVIDENCE_LABEL,
    )
    ppt_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["ppt"])],
        verbose_name=evidence_consts.PPT_FILE_EVIDENCE_LABEL,
    )
    pptx_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["pptx"])],
        verbose_name=evidence_consts.PPTX_FILE_EVIDENCE_LABEL,
    )
    odp_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["odp"])],
        verbose_name=evidence_consts.ODP_FILE_EVIDENCE_LABEL,
    )
    jpg_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg"])],
        verbose_name=evidence_consts.JPG_FILE_EVIDENCE_LABEL,
    )
    jpeg_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["jpeg"])],
        verbose_name=evidence_consts.JPEG_FILE_EVIDENCE_LABEL,
    )
    png_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        verbose_name=evidence_consts.PNG_FILE_EVIDENCE_LABEL,
    )
    gif_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["gif"])],
        verbose_name=evidence_consts.GIF_FILE_EVIDENCE_LABEL,
    )
    bmp_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["bmp"])],
        verbose_name=evidence_consts.BMP_FILE_EVIDENCE_LABEL,
    )
    webp_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["webp"])],
        verbose_name=evidence_consts.WEBP_FILE_EVIDENCE_LABEL,
    )
    zip_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["zip"])],
        verbose_name=evidence_consts.ZIP_FILE_EVIDENCE_LABEL,
    )
    rar_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["rar"])],
        verbose_name=evidence_consts.RAR_FILE_EVIDENCE_LABEL,
    )
    sevenzip_file_evidence = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=["7z"])],
        verbose_name=evidence_consts.SEVENZIP_FILE_EVIDENCE_LABEL,
    )
    misc = models.FileField(
        upload_to="evidences/",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_MISC_FILE_EXTENSIONS)],
        verbose_name=evidence_consts.MISC_FILE_EVIDENCE_LABEL,
    )

    class Meta:
        db_table = "evidence"
        verbose_name = evidence_consts.MODEL_VERBOSE_NAME
        verbose_name_plural = evidence_consts.MODEL_VERBOSE_NAME_PLURAL
        ordering = ["created_at"]

    def __str__(self):
        """Return the case name used to identify this evidence record.

        Returns:
            str: Human-readable identifier for the evidence.
        """
        return f"{self.case_name}"
