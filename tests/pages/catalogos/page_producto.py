from enum import Enum

from tests.pages.catalogos.page_tipo_producto import FieldTipoProductoEnum, PageTipoProducto
from tests.pages.core.constants import DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldProductosEnum(Enum):
    """Enum de campos para el módulo de Productos."""

    PRODUCTO = "producto"
    TIPO_PRODUCTO = "tipo_producto"
    FECHA_CREACION = "fecha_creacion"


class FieldListaNegraEnum(Enum):
    """Enum de campos para lista negra."""

    TIPO_LISTA_NEGRA = "tipo_lista_negra"
    NOMBRES = "nombres"
    PATERNO = "paterno"
    MATERNO = "materno"
    FOTO_ROSTRO = "foto_rostro"
    NUMERO_PLACA = "numero_placa"

    TIPO_PLACA = "placa"
    TIPO_ROSTRO = "rostro"


class PageProducto(GenericPage):
    """Page Object para el módulo de Productos."""

    def __init__(self, page):
        super().__init__(
            page,
            navigation=["Catálogos", "Productos"],
        )
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.sidebar_button_selector = 'a:has-text("Catálogos")'
        self.index_page_button_selector = 'a[title="Productos"]'
        self.index_page_title_selector = 'h1:has-text("Productos")'
        self.create_form_button_selector = 'a:has-text("Agregar producto")'
        self.detail_button_selector = 'a[title="Show"]'
        self.edit_button_selector = 'a[title="Update"]'
        self.detail_page_title_selector = 'h1:has-text("Detalles del producto")'
        self.edit_form_title_selector = 'h1:has-text("Editar producto")'
        self.enable_button_selector = 'input[title=" Habilitar "]'

        self.input_field_dependencies = {
            PageTipoProducto: {
                DependencyAction.CREATE: {
                    FieldProductosEnum.TIPO_PRODUCTO.value: [FieldTipoProductoEnum.NOMBRE.value],
                }
            }
        }

        self.input_field_instances = {
            FieldProductosEnum.PRODUCTO.value: FieldsPage(
                self.page,
                name=FieldProductosEnum.PRODUCTO.value,
            ),
            FieldProductosEnum.TIPO_PRODUCTO.value: FieldsPage(
                self.page,
                name=FieldProductosEnum.TIPO_PRODUCTO.value,
                input_type=InputType.SELECT,
                num_dependencies=1,
                is_filter=False,
            ),
            FieldProductosEnum.FECHA_CREACION.value: FieldsPage(
                self.page,
                name=FieldProductosEnum.FECHA_CREACION.value,
                input_type=InputType.DATE,
                allowed_values=[5],
                is_indexable=False,
                is_data_validate=False,
            ),
        }
