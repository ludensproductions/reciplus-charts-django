"""Mixin de navegación para GenericPage.

Contiene métodos para navegar entre diferentes páginas del módulo
y realizar búsquedas con filtros.
"""


class NavigationMixin:
    """Mixin que proporciona métodos de navegación entre páginas.

    Requiere que la clase que lo herede tenga los siguientes atributos:
        - self.page (Page): Instancia de Playwright
        - self.navigation (list): Lista de rutas para llegar al índice
        - self.disabled_index_page_button_selector (str): Selector del botón de índice deshabilitado
        - self.disabled_index_page_title_selector (str): Selector del título de página deshabilitada
        - self.create_form_button_selector (str): Selector del botón de crear
        - self.detail_page_title_selector (str): Selector del título de página de detalle
        - self.edit_form_title_selector (str): Selector del título de formulario de edición
        - self.data_filters (dict): Diccionario de filtros actuales
        - self.filter_button_selector (str): Selector del botón de filtrar
        - self.index_data_validate (dict): Datos para validar en el índice

    Y los siguientes métodos:
        - wait_for_selector()
        - get_detail_button_selector()
        - get_edit_button_selector()
        - fill_data()
        - validate_record_information_in_index_view()
    """

    NAVIGATION_SELECTOR = 'a:has(span:text-is("{route}")), a:has(h2:text-is("{route}"))'

    async def goto_index_page(self):
        """Navega a la página principal del módulo utilizando las rutas definidas en `self.navigation`.

        Efectos:
            - Recorre la lista de rutas en `self.navigation`.
            - Espera el selector correspondiente y hace clic en cada uno para llegar al índice.
        """
        for route in self.navigation:
            selector = self.NAVIGATION_SELECTOR.format(route=route)
            await self.wait_for_selector(selector)
            await self.page.click(selector)

    async def goto_disabled_index_page(self):
        """Navega a la página que muestra los registros eliminados o deshabilitados.

        Efectos:
            - Llama a `goto_index_page` para ir al índice principal.
            - Hace clic en el botón de índice deshabilitado.
            - Espera a que el título de la página deshabilitada sea visible.
        """
        await self.goto_index_page()
        await self.wait_for_selector(self.disabled_index_page_button_selector)
        await self.page.click(self.disabled_index_page_button_selector)
        await self.wait_for_selector(self.disabled_index_page_title_selector)

    async def goto_create_page(self):
        """Navega al formulario de creación de un nuevo registro.

        Efectos:
            - Llama a `goto_index_page` para ir al índice principal.
            - Espera el selector del botón de creación.
            - Hace clic en el botón para abrir el formulario de creación.
        """
        await self.goto_index_page()
        await self.wait_for_selector(self.create_form_button_selector)
        await self.page.click(self.create_form_button_selector)

    async def goto_detail_page(self):
        """Navega a la página de detalles de un registro.

        Efectos:
            - Realiza una búsqueda de registros con los filtros actuales.
            - Obtiene y espera el selector del botón de detalle.
            - Hace clic en el botón de detalle.
            - Espera a que el título de la página de detalle sea visible.
        """
        await self.search_records_with_filters(self.data_filters)
        detail_button_selector = await self.get_detail_button_selector()
        await self.wait_for_selector(detail_button_selector)
        await self.page.click(detail_button_selector)
        await self.wait_for_selector(self.detail_page_title_selector, time_sleep=0.10)

    async def goto_edit_page(self):
        """Navega al formulario de edición de un registro.

        Efectos:
            - Busca registros aplicando los filtros actuales.
            - Obtiene y espera el selector del botón de edición.
            - Hace clic en el botón de edición.
            - Espera a que el título del formulario de edición sea visible.
        """
        await self.search_records_with_filters()
        edit_button_selector = await self.get_edit_button_selector()
        await self.wait_for_selector(edit_button_selector)
        await self.page.click(edit_button_selector)
        await self.wait_for_selector(self.edit_form_title_selector)
