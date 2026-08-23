from enum import Enum

from pages.catalogos.page_peliculas import FieldPeliculasEnum, PagePeliculas  # Es posible que requiera ajustes
from pages.core.constants import FileTypeEnum

from tests.pages.core.constants import AllowedDatesFormates, DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldInventarioPeliculasEnum(Enum):
    """Enumeration of fields for the Inventario Peliculas page."""

    MOVIE = "movie"
    PRODUCTOR = "productor"
    QUANTITY = "quantity"
    EMAIL = "email"
    PASSWORD = "password"
    REGISTRATION_DATE = "registration_date"
    MODIFICATION_DATE = "modification_date"
    PHONE = "phone"
    BILLING_FILE = "billing_file"
    MOVIE_COVER = "movie_cover"
    RFC = "rfc"
    CURP = "curp"


class PageInventarioPeliculas(GenericPage):
    """Page object for the Inventario Peliculas catalog page."""

    def __init__(self, page):
        super().__init__(
            page, module_name="Inventario de peliculas", navigation=["Catálogos", "Inventario de películas"]
        )
        self.detail_page_title_selector = 'h1:has-text("Detalles del inventario de la película")'
        self.delete_mode = DeleteModeEnum.DISABLE_INDEX
        self.disabled_index_page_title_selector = 'h1:has-text("Inventario de películas deshabilitadas")'

        self.input_field_dependencies = {
            PagePeliculas: {
                DependencyAction.CREATE: {
                    FieldInventarioPeliculasEnum.MOVIE.value: [
                        FieldPeliculasEnum.YEAR.value,
                        " - ",
                        FieldPeliculasEnum.TITLE.value,
                    ],
                },
                DependencyAction.FILTER: {
                    FieldInventarioPeliculasEnum.MOVIE.value: [
                        FieldPeliculasEnum.YEAR.value,
                        " - ",
                        FieldPeliculasEnum.TITLE.value,
                    ],
                },
                DependencyAction.INDEX: {
                    FieldInventarioPeliculasEnum.MOVIE.value: [
                        FieldPeliculasEnum.TITLE.value,
                    ],
                },
            }
        }

        self.input_field_instances = {
            FieldInventarioPeliculasEnum.MOVIE.value: FieldsPage(
                page=page,
                name=FieldInventarioPeliculasEnum.MOVIE.value,
                input_type=InputType.SELECT2,
                filter_type=InputType.SELECT,
                field_selector="#div_id_movie",
                max_length=255,
                min_length=2,
                field_truncate_suffix="...",
                index_truncate_suffix="",
                validate_truncate_suffix="",
                filter_truncate_length=43,
                field_truncate_length=68,
                index_truncate_length=100,
                validate_truncate_length=100,
            ),
            FieldInventarioPeliculasEnum.PRODUCTOR.value: FieldsPage(
                page=page,
                name=FieldInventarioPeliculasEnum.PRODUCTOR.value,
                max_length=255,
                min_length=2,
            ),
            FieldInventarioPeliculasEnum.QUANTITY.value: FieldsPage(
                page=page,
                is_filter=False,
                name=FieldInventarioPeliculasEnum.QUANTITY.value,
                input_type=InputType.NUMBER,
                max_value=99999,
                min_value=2,
            ),
            FieldInventarioPeliculasEnum.EMAIL.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.EMAIL.value,
                input_type=InputType.EMAIL,
                max_length=255,
                min_length=2,
            ),
            FieldInventarioPeliculasEnum.PASSWORD.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.PASSWORD.value,
                input_type=InputType.PASSWORD,
                min_length=10,
                is_data_validate=False,
            ),
            FieldInventarioPeliculasEnum.REGISTRATION_DATE.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.REGISTRATION_DATE.value,
                input_type=InputType.DATE,
                min_value=2,
                max_value=255,
                detail_format_date=AllowedDatesFormates.DATE_IN_SPANISH,
            ),
            FieldInventarioPeliculasEnum.MODIFICATION_DATE.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.MODIFICATION_DATE.value,
                input_type=InputType.DATE,
                is_required=False,
                max_value="2026-12-31",
                detail_format_date=AllowedDatesFormates.DATE_IN_SPANISH,
            ),
            FieldInventarioPeliculasEnum.PHONE.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.PHONE.value,
                input_type=InputType.REGEX,
                max_length=10,
                min_length=10,
                regex_pattern=r"^\d{10}$",
            ),
            FieldInventarioPeliculasEnum.RFC.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.RFC.value,
                input_type=InputType.REGEX,
                max_length=13,
                min_length=12,
                regex_pattern=r"^(([A-ZÑ&]{3}(((([02468][048])|([13579][26]))0229|(\d{2})((02(0[1-9]|1\d|2[0-8]))|(((0[13456789])|1[012])(0[1-9]|[12]\d|30))|(((0[13578])|(1[02]))31))))[A-Z\d]{3})|((?!((([CcKk][Aa][CcKkGg][AaOo])|([Bb][Uu][Ee][YyIi])|([Kk][Oo](([Gg][Ee])|([Jj][Oo])))|([Cc][Oo](([Gg][Ee])|([Jj][AaEeIiOo])))|([QqCcKk][Uu][Ll][Oo])|((([Ff][Ee])|([Jj][Oo])|([Pp][Uu]))[Tt][Oo])|([Rr][Uu][Ii][Nn])|([Gg][Uu][Ee][Yy])|((([Pp][Uu])|([Rr][Aa]))[Tt][Aa])|([Pp][Ee](([Dd][Oo])|([Dd][Aa])|([Nn][Ee])))|([Mm](([Aa][Mm][OoEe])|([Ee][Aa][SsRr])|([Ii][Oo][Nn])|([Uu][Ll][Aa])|([Ee][Oo][Nn])|([Oo][Cc][Oo]))))))[A-ZÑ&]{1}[AEIOU]{1}[A-ZÑ&]{2}(((([02468][048])|([13579][26]))0229|(\d{2})((02(0[1-9]|1\d|2[0-8]))|(((0[13456789])|1[012])(0[1-9]|[12]\d|30))|(((0[13578])|(1[02]))31))))[A-Z\d]{3})|([Xx][AaEe][Xx]{2}010101000))$",
                is_data_validate=False,
            ),
            FieldInventarioPeliculasEnum.CURP.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.CURP.value,
                input_type=InputType.REGEX,
                max_length=18,
                min_length=18,
                regex_pattern=r"^[A-Z][AEIOU][A-Z]{2}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$",
                is_data_validate=False,
            ),
            FieldInventarioPeliculasEnum.BILLING_FILE.value: FieldsPage(
                page=page,
                is_filter=False,
                allowed_values=[FileTypeEnum.PDF.value, FileTypeEnum.ZIP.value],
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.BILLING_FILE.value,
                input_type=InputType.FILE,
                max_value=48.00,
            ),
            FieldInventarioPeliculasEnum.MOVIE_COVER.value: FieldsPage(
                page=page,
                is_filter=False,
                allowed_values=[FileTypeEnum.JPG.value, FileTypeEnum.PNG.value],
                is_indexable=False,
                name=FieldInventarioPeliculasEnum.MOVIE_COVER.value,
                input_type=InputType.FILE,
                is_data_validate=False,
            ),
        }
