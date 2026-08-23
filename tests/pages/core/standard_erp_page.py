import base64
import json

from playwright.async_api import Page

from tests.pages.core.base_page import BasePage


class StandardErpPage(BasePage):
    """A class that encapsulates interactions with a web page.

    Provides methods for form manipulation, data validation, and user interaction.

    This class is designed to facilitate the automation of web interactions using
    Playwright. Each method within this class operates on the current page context
    and assumes that the user is already on the appropriate page or form.

    Attributes:
        page (Page): An instance of the Playwright Page class, representing the current page.
    """

    def __init__(self, page: Page):
        self.page = page

        # Generic selectors
        self.sgi_logo_selector = 'a[title="SGI"]'
        self.minimize_modal_selector = 'button[class="btn btn-secondary btn-sm pull-right grid-collapse-row"]'
        self.open_modal_selector = 'div[data-original-title="Editar"] a'
        self.add_row_selector = 'button:has-text("Añadir fila")'
        self.save_button_selector = 'button[data-label="Guardar"]'
        self.actions_button_selector = 'button:has-text("Acciones")'
        self.delete_button_selector = 'a:has-text("Eliminar")'
        self.si_button_selector = 'button[class="btn btn-primary btn-sm btn-modal-primary"]'
        self.identifier_input_selector = 'input[data-fieldname="name"]'
        self.input_file_selector = 'input[type="file"]'
        self.upload_file_selector = '.modal.show button:has-text("Subir")'

    async def fill_data(self, data: dict):
        """Llama al método genérico de la clase base y añade o modifica lo necesario."""
        # Primero llama al método fill_data de la clase base
        await super().fill_data(data)

        # Funcionalidades adicionales
        for field_name, value in data.items():
            field_input = self.page.locator(field_name)
            tag_name = await field_input.evaluate("el => el.tagName")
            input_type = await field_input.evaluate("el => el.type")
            data_fieldtype = await field_input.evaluate('(el) => el.getAttribute("data-fieldtype")')

            if input_type == "button" or tag_name in ["BUTTON", "A"]:
                if data_fieldtype in ["Attach", "Attach Image"]:
                    await self.attach_file(field_name, value)
                elif isinstance(value, list):
                    await field_input.click()
                    for fila_data in value:
                        await self.fill_data(fila_data)
                else:
                    await self.page.click(field_name)

            elif tag_name == "DIV":
                if data_fieldtype == "Text Editor":
                    if value:
                        await self.page.click(f'{field_name} div[contenteditable="true"]')
                        await self.page.keyboard.type(value)
                    else:
                        current_content = await self.page.locator(
                            f'{field_name} div[contenteditable="true"]'
                        ).text_content()
                        await self.page.click(f'{field_name} div[contenteditable="true"]')
                        for _ in range(len(current_content)):
                            await self.page.keyboard.press("Backspace")

            elif tag_name == "CANVAS":
                restart_button_selector = field_name.replace("canvas", "a")
                await self.page.click(restart_button_selector)
                if value:
                    await self.draw_signature_from_base64(field_name, value)

    async def draw_signature_from_base64(self, canvas_selector: str, signature_base64: str):
        """Dibuja una firma en el canvas a partir de una cadena base64.

        Args:
            canvas_selector (str): El selector para el elemento canvas.
            signature_base64 (str): La firma codificada en base64.
        """
        # Decodificar la firma base64
        signature_json = base64.b64decode(signature_base64).decode()
        signature_data = json.loads(signature_json)

        # Obtener la posición del canvas
        canvas = self.page.locator(canvas_selector)
        bounding_box = await canvas.bounding_box()

        # Establecer variables de escala para ajustar las coordenadas al tamaño del canvas
        start_x = bounding_box["x"] + 10
        start_y = bounding_box["y"] + 10
        width = bounding_box["width"] - 20
        height = bounding_box["height"] - 20

        # Mover el ratón al canvas y presionar para empezar a dibujar
        await self.page.mouse.move(start_x + signature_data[0]["x"], start_y + signature_data[0]["y"])
        await self.page.mouse.down()

        # Dibujar los puntos de la firma decodificada
        for point in signature_data:
            x = start_x + (point["x"] / 100) * width  # Escalar las coordenadas
            y = start_y + (point["y"] / 50) * height
            await self.page.mouse.move(x, y, steps=5)

        # Soltar el ratón para terminar el dibujo
        await self.page.mouse.up()

    async def edit_item(self, new_data: dict):
        """Edits an item with new data."""
        await super().edit_item(new_data)

    async def validate_edit_view_item_information(self, data_validate: dict):
        """Validates the information of an item in edit view."""
        # Llamada al método de la clase padre
        await super().validate_edit_view_item_information(data_validate)

        for field_name, expected_value in data_validate.items():
            field_input = self.page.locator(field_name)
            tag_name = await field_input.evaluate("el => el.tagName")

            # Sección para manejar botones y enlaces
            if tag_name == "BUTTON" or tag_name == "A":
                if isinstance(expected_value, list):
                    for fila_data in expected_value:
                        await field_input.click()
                        await self.validate_edit_view_item_information(fila_data)
                        selector = field_name.split(" ", 1)[0]
                        await self.page.click(f"{selector} {self.minimize_modal_selector}")
                else:
                    await field_input.click()
                continue

            # Manejo de campos tipo DIV
            if tag_name == "DIV":
                data_fieldtype = await field_input.evaluate('(el) => el.getAttribute("data-fieldtype")')
                if data_fieldtype == "Text Editor":
                    editable_div = self.page.locator(f'{field_name} div[contenteditable="true"]')
                    actual_value = await editable_div.text_content()
                    assert actual_value == expected_value, f"Expected '{expected_value}', but got '{actual_value}'"
                elif data_fieldtype == "Data":
                    actual_value = await field_input.text_content()
                    assert actual_value == expected_value, f"Expected '{expected_value}', but got '{actual_value}'"
                elif data_fieldtype == "Attach Image":
                    actual_value = await field_input.locator(f"a:has-text('{expected_value}')").text_content()
                    assert actual_value.endswith(
                        expected_value
                    ), f"Expected '{expected_value}', but got '{actual_value}'"

            # Manejo de campos tipo CANVAS
            elif tag_name == "CANVAS":
                signature = await self.get_firma_base64(field_name)
                assert signature is not None, f"No hay firma. {signature[:5]}"

    async def attach_file(self, selector, path):
        """Attach file on for register."""
        await self.page.click(selector)
        await self.fill_data({self.input_file_selector: path})
        button = self.page.locator(self.upload_file_selector)
        await button.click()
        await self.page.wait_for_timeout(1000)

    async def get_firma_base64(self, selector: str):
        """Fill a canvas element with a signature or drawing.

        Args:
            selector (str): The selector for the canvas element where the signature or drawing will be applied.

        Example:
            selector = 'canvas.signature-canvas'

        Return:
            This method returns the value of the new signature in base64

        Note:
            - Ensure that the provided `canvas_selector` corresponds to the canvas element where the signature or drawing is expected.
            - This method is intended for use with canvas elements that capture user input, such as signature pads.
        """
        # Localizar el canvas que contiene la firma
        canvas_element = self.page.locator(selector)

        # Obtener la firma del canvas en formato base64
        signature_base64 = await canvas_element.evaluate('canvas => canvas.toDataURL("image/png")')

        # Imprimir o devolver la imagen en base64 (puedes guardarla en un archivo si lo prefieres)
        return signature_base64
