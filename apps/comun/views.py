import base64
import json
from collections import defaultdict
from datetime import timedelta
from typing import Any, Dict, Iterable, List, Tuple, Union
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import FileField, ImageField, JSONField, ManyToManyField
from django.forms import all_valid, formset_factory, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, resolve_url
from django.urls import NoReverseMatch, reverse
from django.utils import timezone as dj_timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.views import generic
from django_filters.views import FilterView
from django_q.tasks import async_task
from simple_history.utils import bulk_create_with_history, bulk_update_with_history

from apps.comun.consts import (
    ACTION_CREATED_LABEL,
    ACTION_DELETE_VERB,
    ACTION_DELETED_LABEL,
    ACTION_RESTORE_VERB,
    ACTION_RESTORED_LABEL,
    ACTION_UPDATED_LABEL,
    ERROR_ACTION_BLOCKED,
    ERROR_DISABLE_ALREADY_DISABLED,
    ERROR_REPORT_DEBUG_NO_RESPONSE,
    ERROR_REPORT_GENERATION,
    ERROR_REPORT_NO_VALID_DATA,
    ERROR_USER_DELETED,
    ERROR_USER_INACTIVE,
    FIELD_DISABLE_LABEL,
    LIST_CONJUNCTION_AND,
    REPORT_EMAIL_SUBJECT,
    REPORT_FILE_NAME,
    SUCCESS_ITEM_ACTION,
    SUCCESS_REPORT_SENT,
)
from apps.comun.filters import create_generic_filter
from apps.core.errors.error_codes import ErrorCode
from apps.core.errors.error_types import ErrorType
from apps.oauth2.const import SESSION_KEY_LOGIN_AT
from apps.users.consts import ERROR_USER_BANNED
from apps.users.models import User
from utils.json_logger import get_error_log, log_warning

from .forms import EmptyForm, GenericBaseFormSet, GenericBaseInlineFormSet, forms
from .formset_utils import get_records_formset_by_prefix
from .utils import create_field, get_user_timezone, send_get_request


class GenericAttributesView:
    """Base class to add extra attributes to Class-Based Views.

    Attributes:
        return_url (str): Default URL to return to the previous page
        title (str): Page title
        verbose_name (str): Name to reference the model; defaults to the model's verbose name if not set
        model (Model): Django model class to work with
        custom_js_files (list): List of custom JavaScript files to include in
            the template
        custom_css_files (list): List of custom CSS files to include in
            the template

    """

    return_url: str = None
    title: str = None
    verbose_name: str = None
    model = None
    custom_js_files: list = []
    custom_css_files: list = []

    def get_verbose_name(self) -> str:
        """The function `get_verbose_name` returns the verbose name of a model instance or falls back to the model's verbose name if not specified.

        @return The `get_verbose_name` method returns the `verbose_name` attribute of the instance if it
        exists, otherwise it returns the `verbose_name` attribute of the model's `_meta` attribute.
        """
        return self.verbose_name or self.model._meta.verbose_name  # noqa: SLF001

    def get_return_url(self) -> str:
        """The function `get_return_url` returns a specified return URL or a default URL if none is provided.

        @return The function `get_return_url` is returning the value of `self.return_url` if it is not
        empty, otherwise it is returning `f"{self.model._meta.app_label}:index"`.
        """
        return self.return_url or f"{self.model._meta.app_label}:index"  # noqa: SLF001

    def get_title(self) -> str:
        """The function `get_title` returns the title of an object or the verbose name of its model in lowercase if the title is not set.

        @return The `get_title` method is returning the title of an object if it exists, otherwise it is
        returning the verbose name of the model in lowercase.
        """
        return (
            self.title or self.model._meta.verbose_name.lower()  # noqa: SLF001
        )

    def get_custom_js_files(self) -> list:
        """The function `get_custom_js_files` returns the list of custom JavaScript files.

        @return The method `get_custom_js_files` is returning the value of the `custom_js_files` attribute.
        """
        return self.custom_js_files

    def get_custom_css_files(self) -> list:
        """The function `get_custom_css_files` returns the list of custom CSS files.

        @return The method `get_custom_css_files` is returning the value of the `custom_css_files` attribute.
        """
        return self.custom_css_files


class GenericInfoView(GenericAttributesView):
    """Base class for info views, such as Detail or Index views.

    Attributes:
        shown_fields (list | dict): Fields to be shown in detail or index view
            ej:
                shown_fields: {
                    "title": "Título",
                    "year": "Año",
                    "price": "Precio",
                    "genre": "Género",
                    "plot": "Trama",
                    "sales_count": "Total de ventas"
                }
        model (Model): Django model class to work with

    """

    shown_fields: list | dict = None
    model = None

    def __order_fields(self, field):
        """The function __order_fields returns the index of a field name within a list or dictionary based on the shown_fields attribute of the object.

        @param field The `field` parameter in the `__order_fields` method is expected to be an object
        representing a field. The method then checks if the `shown_fields` attribute of the object is a
        list or a dictionary, and returns the index of the `field.name` within the `shown_fields`

        @return The code snippet is a method named "__order_fields" that takes a "field" parameter. It
        checks if the "shown_fields" attribute of the object is a list or a dictionary. If it is a list,
        the method returns the index of the "field.name" within the list. If it is a dictionary, the
        method returns the index of the "field.name" within the keys of
        """
        if isinstance(self.shown_fields, list):
            return self.shown_fields.index(field.name)
        elif isinstance(self.shown_fields, dict):
            return list(self.shown_fields.keys()).index(field.name)

    def get_fields(self) -> list:
        """Retrieves fields and properties based on shown_fields attribute.

        Maintains order and supports both regular fields and model properties.
        """
        if not self.shown_fields:
            msg = "You must define shown_fields or override get_fields"
            raise NotImplementedError(msg)

        # Get all regular fields as a dictionary for faster lookup
        model_fields = {f.name: f for f in self.model._meta.get_fields()}  # noqa: SLF001

        if isinstance(self.shown_fields, list):
            fields = [
                create_field(self, name, model_fields)
                for name in self.shown_fields
                if create_field(self, name, model_fields) is not None
            ]
        elif isinstance(self.shown_fields, dict):
            print("self.shown_fields", self.shown_fields)
            fields = [
                create_field(self, name, model_fields, verbose_name)
                for name, verbose_name in self.shown_fields.items()
                if create_field(self, name, model_fields, verbose_name) is not None
            ]
        else:
            msg = "shown_fields must be a list or a dictionary"
            raise ValueError(msg)

        # Keep order of shown_fields
        return sorted(fields, key=self.__order_fields)

    def get_field_attributes(self) -> dict:
        """Obtiene los atributos personalizados de los campos."""
        return getattr(self, "field_attributes", {})


class GenericFormView(SuccessMessageMixin, GenericAttributesView):
    """Generic base view for form-based Class-Based Views.

    Attributes:
        model (Model): Django model class to work with
        template_name (str): Template to load HTML, default is "generic/form.html"
        form_class (Form): Form class to work with, this form will be loaded in HTML
        success_url (str): URL to redirect after successful form submission
        success_message (str): Message to display after successful form submission
    """

    model = None
    template_name: str = "generic/form.html"
    form_class = None
    success_url = None
    success_message = SUCCESS_ITEM_ACTION

    def get_form_kwargs(self) -> dict:
        """The function `get_form_kwargs` adds the current user to the keyword arguments for a form in a Django view.

        @return The `kwargs` dictionary with an additional key-value pair where the key is "user" and
        the value is `self.request.user` is being returned.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs) -> dict:
        """The function `get_context_data` adds additional context data to a dictionary and returns it.

        @return The `get_context_data` method is returning a dictionary `context` that contains the
        following key-value pairs:
        - "verbose_name": the result of calling the `get_verbose_name` method on `self`
        - "return_url": the result of calling the `get_return_url` method on `self`
        - "title": the result of calling the `get_title` method on `self`
        """
        context = super().get_context_data(**kwargs)
        context["verbose_name"] = self.get_verbose_name()
        return_url = self.get_return_url()
        context["return_url"] = return_url
        context["title"] = self.get_title()
        context["custom_js_files"] = self.get_custom_js_files()
        context["custom_css_files"] = self.get_custom_css_files()
        return context

    def get_success_message(self, cleaned_data) -> str:
        """Returns a formatted success message for the created object.

        This implementation uses `str.format_map()` with a `defaultdict` to safely handle missing keys in the context.

        @param cleaned_data The `cleaned_data` parameter is a dictionary that contains the cleaned and validated data from the form.
        """
        context = {}
        context["action"] = getattr(self, "action", "guardado")
        if cleaned_data:
            context.update(cleaned_data)
        safe_context = defaultdict(str, context)
        return self.success_message.format_map(safe_context)

    def form_invalid(self, form):
        """Handle invalid form submission and log validation errors."""
        log_warning(
            {
                "type": ErrorType.VALIDATION_ERROR,
                "code": ErrorCode.VAL_001,
                "log_message": json.loads(form.errors.as_json()),
                **get_error_log(self.request),
            }
        )
        return super().form_invalid(form)


# End attributes classes


# Start generic views
class CustomLoginView(auth_views.LoginView):
    """Custom login based view.

    Attributes:
        template_name (str): Template to load HTML, default is "registration/login.html"
        success_url (str | None): URL to redirect after successful login, default is None

    Note:
        This class inherits from auth_views.LoginView and may use its form_class.
        The actual redirection is handled by the get_success_url method.
    """

    template_name = "registration/login.html"
    success_url = None  # Can be set to reverse_lazy('root') if needed

    def get_success_url(self) -> str:
        """The function `get_success_url` returns the next URL if provided in the request, the success URL if set, or the default login redirect URL.

        @return The `get_success_url` method returns the next URL if it is provided in the request's GET
        parameters. If not, it checks if `self.success_url` is set and returns it if available. If
        neither the next URL nor `self.success_url` is provided, it returns the default login redirect
        URL specified in the settings.
        """
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url

        if self.success_url:
            return resolve_url(self.success_url)

        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get(self, request, *args, **kwargs):
        """This function checks if the user is authenticated and redirects to a success URL if they are, otherwise it calls the parent class's get method.

        @param request The `request` parameter in the `get` method is an object that contains
        information about the current HTTP request, such as the user making the request, the requested
        URL, request method (GET, POST, etc.), headers, and any data sent with the request. It is
        typically passed to view

        @return If the user is authenticated, a redirect to the success URL is being returned.
        Otherwise, the `get` method of the superclass is being called and returned.
        """
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """The function `form_valid` checks if a user is deleted or inactive before proceeding with form validation.

        @param form The `form_valid` method in the code snippet is a part of a Django class-based view.
        It is used to handle the form submission logic when the form data is valid.

        @return The `form_valid` method is returning the result of calling the `form_valid` method of
        the superclass (in this case, `super().form_valid(form)`).
        """
        username = form.cleaned_data["username"]

        user = User.objects.get(username=username)

        if user.deleted is not None:
            form.add_error("username", str(ERROR_USER_DELETED))
            return self.form_invalid(form)

        if user.is_active is False:
            form.add_error("username", str(ERROR_USER_INACTIVE))
            return self.form_invalid(form)

        if user.is_banned:
            messages.error(self.request, str(ERROR_USER_BANNED))
            return self.form_invalid(form)

        response = super().form_valid(form)
        self.request.session[SESSION_KEY_LOGIN_AT] = dj_timezone.now().isoformat()
        return response


class GenericDetailView(GenericInfoView, generic.DetailView):
    """Base class for DetailView.

    Attributes:
        shown_fields (list | dict): Fields to be shown in detail view
        model (Model): Django model class to work with
        template_name (str): Template to load HTML, default is "generic/detail.html"

    """

    shown_fields: list | dict = None
    model = None
    template_name: str = "generic/detail.html"
    view_deleted_objects = False

    def get_context_data(self, **kwargs) -> dict:
        """The `get_context_data` function in Python retrieves and returns various context data for a view, such as title, return URL, fields, and verbose name.

        @return A dictionary named `context` is being returned. It contains keys such as "title",
        "return_url", "fields", and "verbose_name", each with corresponding values obtained from the
        methods `get_title()`, `get_return_url()`, `get_fields()`, and `get_verbose_name()`.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()

        context["return_url"] = self.get_return_url()

        context["fields"] = self.get_fields()

        context["field_attributes"] = self.get_field_attributes()

        context["verbose_name"] = self.get_verbose_name()

        context["m2m_separator"] = self.get_m2m_separator()

        return context

    def get_queryset(self):
        """The function `get_queryset` retrieves the queryset for the current view.

        @return The `get_queryset` method is returning the default queryset for the model if
        `view_deleted_objects` is False. If `view_deleted_objects` is True, it returns all objects
        including those that have been deleted.
        """
        if not self.view_deleted_objects:
            return super().get_queryset()

        return self.model.all_objects.all()

    def get_m2m_separator(self):
        """Get the separator string used to join ManyToMany field values in display.

        Returns:
            str: The separator string to use when joining M2M values. Defaults to ", " if not explicitly set.

        Example:
            You can customize the separator by setting the `m2m_separator` attribute on the view:

        ```python
        class MyDetailView(GenericDetailView):
            m2m_separator = " | "  # Use pipe instead of comma
        ```

        This affects how related objects are displayed in detail views when showing ManyToMany relationships.
        For example, if a movie has multiple genres, they might be displayed as "Action, Comedy, Drama"
        or "Action | Comedy | Drama" depending on the separator.
        """
        return getattr(self, "m2m_separator", ", ")

    def get_field_value(self, item, field):
        """Obtiene el valor de un campo del objeto, manejando callables, M2M y formatos especiales."""
        value = getattr(item, field)

        if callable(value) and not hasattr(value, "all"):
            return str(value())
        elif hasattr(value, "all"):  # M2M or reverse FK
            # Ordenar por id de forma ascendente para mantener consistencia
            return self.get_m2m_separator().join(str(obj) for obj in value.all().order_by("id"))
        # Hacemos este parseo por que al obtenerlo de la bd si el valor es 09:37:18 lo devuelve como 9:37:18
        elif isinstance(value, timedelta):
            # Formatear timedelta con ceros a la izquierda (HH:MM:SS)
            total_seconds = int(value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return str(value)


class GenericMultiEntityDetailView(GenericDetailView):
    """Base class for MultiEntityDetailView with formset support.

    Attributes:
        shown_fields (list | dict): Fields to be shown in detail view.
        children_entities (list | dict): Related models to be displayed as formsets.
        model (Model): Django model class to work with.
        template_name (str): Template to load HTML, default is "generic/detail.html".
        table_title (dict): Field to be detail in the title table.
    """

    # shown_fields = {
    #     "model field": "name of field",
    # }

    # children_entities = {
    #     "related_name of ForeignKey": {
    #         "name of field": "name in español"
    #     }
    # }

    # table_title = {
    #     "title": "title in español",
    # }

    shown_fields: list | dict = None
    children_entities: list | dict = None
    model = None
    table_title: dict = None
    template_name: str = "generic/detail.html"

    def get_context_data(self, **kwargs) -> dict:
        """Retrieves context data including formsets for child entities.

        @return A dictionary with context data including title, return URL, fields, verbose name,
                and formsets for related entities.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        context["return_url"] = self.get_return_url()
        context["fields"] = self.get_fields()
        context["field_attributes"] = self.get_field_attributes()
        context["verbose_name"] = self.get_verbose_name()

        # Manejo de formsets para children_entities
        if self.children_entities:
            child_entities = {}

            # Si children_entities es una lista, la convertimos en un diccionario con `__all__`
            if isinstance(self.children_entities, list):
                self.children_entities = {entity: "__all__" for entity in self.children_entities}

            for manager_name, fields in self.children_entities.items():
                related_manager = getattr(self.object, manager_name, None)

                if related_manager is not None and hasattr(related_manager, "model"):
                    if isinstance(fields, dict):
                        field_names = list(fields.keys())  # Convertir dict a lista de nombres de campos
                        field_labels = list(fields.values())
                    else:
                        continue  # Si no es una lista válida, saltamos este conjunto de datos

                    # Obtener los valores del queryset en lugar de un formset
                    related_data = [
                        {field: self.get_field_value(item, field) for field in field_names}
                        for item in related_manager.all()
                    ]
                    print("related_data", related_data)
                    # Agregar los datos al contexto
                    child_entities[manager_name] = {
                        "fields": field_names,  # Nombres de los campos
                        "labels": field_labels,
                        "data": related_data,
                        "table_title": self.get_table_title().get(manager_name),  # Datos de la relación
                    }

            context["child_entities"] = child_entities
        return context

    def get_table_title(self) -> dict:
        """The function `get_table_title` returns the table title if it exists, otherwise it returns an empty dictionary.

        @return The `get_table_title` method is returning the value of `self.table_title` if it exists,
        """
        if not self.table_title:
            raise NotImplementedError("You must define table_title or override get_table_title")

        return self.table_title or {}


class GenericCreateView(GenericFormView, generic.CreateView):
    """Base class for CreateView.

    Attributes:
        template_name (str): Template to load HTML, default is "generic/form.html"

    Note:
        This class inherits attributes and methods from GenericFormView and generic.CreateView.
        Only attributes specific to this class or overridden are listed here.
    """

    template_name: str = "generic/form.html"
    action = ACTION_CREATED_LABEL


class GenericUpdateView(GenericFormView, generic.UpdateView):
    """Base class for UpdateView.

    Attributes:
        template_name (str): Template to load HTML, default is "generic/form.html"

    Note:
        This class inherits attributes and methods from GenericFormView and generic.UpdateView.
        Only attributes specific to this class or overridden are listed here.
    """

    template_name: str = "generic/form.html"
    action = ACTION_UPDATED_LABEL


class GenericFilterView(GenericInfoView, FilterView):
    """Base class for FilterView with additional functionality.

    Attributes:
        shown_fields (list[str]): List of field names to be displayed in the view
        model (Model): Django model class to be used for the view
        create_url (str): URL name for creating new objects
        edit_url (str): URL name for updating existing objects
        delete_url (str): URL name for deleting objects
        detail_url (str): URL name for displaying object details
        return_url (str): URL to return to after certain actions
        template_name (str): Name of the template to be used for rendering
        paginate_by (int): Number of items to display per page
        context_object_name (str): Name of the variable to use for the object list in the template
        can_disable (bool): Flag to indicate if objects can be disabled instead of deleted
        filterset_class (FilterSet): Clase de filtro para aplicar sobre el queryset
        filter_fields (dict): Configuración de los campos que serán usados como filtros
        excluded_filter_list (list[str]): Campos que no serán filtros
        extra_actions (list): Acciones extras que aparecen como botones/iconos en cada fila de la tabla.
            Cada acción es un diccionario con keys: url, params, icon, color, tooltip, validation (opcional)
        general_extra_actions (list): Acciones extras generales que aparecen como botones en el header de la página.
            Cada acción es un diccionario con keys: title_button, icon, url, class

    This class combines functionality from GenericInfoView and FilterView to create
    a flexible, paginated list view with filtering capabilities. It provides various
    URL configurations for CRUD operations and customizable display options.
    """

    shown_fields: list[str] = []
    model = None
    create_url = ""
    edit_url = None
    delete_url = None
    detail_url = None
    disable_url = None
    return_url = None
    template_name: str = "generic/index.html"
    paginate_by = 20
    context_object_name = "items"
    can_disable = False
    is_disabled_view = False
    filterset_class = None
    filter_fields = {}
    excluded_filter_list = [
        "created_by",
        "updated_by",
        "updated_at",
        "created_at",
        "id",
        "deleted",
        "deleted_by_cascade",
    ]
    check_permissions = True
    override_permissions = {}
    excluded_filter_list = [
        "created_by",
        "updated_by",
        "updated_at",
        "created_at",
        "id",
        "deleted",
        "deleted_by_cascade",
    ]
    extra_actions = []
    general_extra_actions = []

    def init_generic_attributes(self):
        """Inicializa los atributos genéricos de URLs basados en el modelo."""
        app_label = self.model._meta.app_label
        self.create_url = f"{app_label}:create"
        self.edit_url = f"{app_label}:edit"
        self.delete_url = f"{app_label}:delete"
        self.detail_url = f"{app_label}:detail"
        self.return_url = f"{app_label}:index"

    def get_permissions(self):
        """The function `get_permissions` retrieves the permissions for the current user based on the model.

        @return The `get_permissions` method returns a dictionary with the keys "add", "change", "delete",
        and "view". The values are boolean values indicating whether the user has the corresponding
        permission for the model.

        """
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        if not self.check_permissions:
            return {
                "add": True,
                "change": True,
                "delete": True,
                "view": True,
            }

        return {
            "add": self.request.user.has_perm(f"{app_label}.add_{model_name}"),
            "change": self.request.user.has_perm(f"{app_label}.change_{model_name}"),
            "delete": self.request.user.has_perm(f"{app_label}.delete_{model_name}"),
            "view": self.request.user.has_perm(f"{app_label}.view_{model_name}"),
        }

    def get_filterset_class(self):
        """Obtiene la clase de filterset para la vista."""
        fields_to_ignore = (ImageField, FileField, JSONField)  # Tupla de clases

        if self.filterset_class:
            return self.filterset_class

        if self.filter_fields:
            for key, value in self.filter_fields.items():
                if isinstance(value, dict):
                    value.setdefault("label", key.capitalize())
                    value.setdefault("placeholder", value["label"])
                else:
                    self.filter_fields[key] = {"label": value.capitalize(), "placeholder": value}

        if not self.filter_fields:
            self.filter_fields = {
                field.name: {"label": field.verbose_name.capitalize(), "placeholder": field.verbose_name}
                for field in self.model._meta.fields
                if (field.name not in self.excluded_filter_list and not isinstance(field, fields_to_ignore))
            }

        if not self.filterset_class:
            self.filterset_class = create_generic_filter(self.model, self.filter_fields)

        return self.filterset_class

    def get_create_url(self) -> str:
        """The function `get_create_url` returns a create URL based on the model's meta app label.

        @return The `get_create_url` method returns a string value. If `self.create_url` is not None, it
        returns the value of `self.create_url`. Otherwise, it returns a formatted string using
        `self.model._meta.app_label` and the string ":create".
        """
        return self.create_url or None

    def get_edit_url(self):
        """The function `get_edit_url` returns the update URL or a default edit URL based on the model's app label.

        @return The `get_edit_url` method is returning either the `edit_url` attribute of the object
        or a formatted string "{self.model._meta.app_label}:edit".
        """
        return self.edit_url

    def get_delete_url(self) -> str:
        """The function `get_delete_url` returns the delete URL or a default delete URL based on the app label and "delete".

        @return The `get_delete_url` method is returning either the `delete_url` attribute of the object
        or a formatted string "{self.model._meta.app_label}:delete".
        """
        return self.delete_url

    def get_detail_url(self) -> str:
        """The function `get_detail_url` returns the detail URL of an object.

        @return The `detail_url` attribute of the object is being returned.
        """
        return self.detail_url  # noqa: SLF001

    def get_return_url(self) -> str:
        """The function `get_return_url` returns the value of the `return_url` attribute of the object.

        @return The method `get_return_url` is returning the value of the attribute `return_url`
        belonging to the instance of the class where this method is defined.
        """
        return self.return_url

    def get_disable_url(self) -> str:
        """The function `get_disable_url` returns the disable URL of an object.

        @return The `disable_url` attribute of the object is being returned.
        """
        if self.can_disable and self.disable_url:
            raise ValueError("The value of `disable_url` and `can_disable` cannot be True at the same time")
        return self.disable_url

    def get_is_disabled_view(self) -> bool:
        """The function `get_is_disabled_view` returns a boolean value indicating whether the view is a disabled view.

        @return The `is_disabled_view` attribute of the object is being returned.
        """
        if self.can_disable and self.is_disabled_view:
            raise ValueError("The value of `is_disabled_view` and `can_disable` cannot be True at the same time")
        return self.is_disabled_view

    def get_general_extra_actions(self) -> list:
        """Construye dinámicamente las acciones extras generales del header.

        Override este método para agregar lógica condicional o usar self.

        Returns:
            list: Lista de diccionarios con acciones del header

        Example:
            You can override this method to build actions dynamically:

        ```python
        def get_general_extra_actions(self):
            actions = []

            # Agregar botón solo si el usuario tiene permiso
            if self.request.user.has_perm('app.export_permission'):
                actions.append({
                    "title_button": "Exportar CSV",
                    "icon": "fas fa-download",
                    "url": "app:export_csv",
                    "class": "btn-primary btn_movil_view_size margin_bottom_btn",
                })

            # Botón condicional basado en configuración
            if self.model._meta.app_label == 'eventos':
                actions.append({
                    "title_button": "Calendario",
                    "icon": "fas fa-calendar",
                    "url": "eventos:calendar",
                    "class": "btn-success btn_movil_view_size margin_bottom_btn",
                })

            return actions
        ```

        These actions will be rendered in the view's template as additional buttons or links,
        allowing users to perform custom operations on the filtered data.
        """
        return getattr(self, "general_extra_actions", [])

    def get_extra_actions(self) -> list:
        """Construye dinámicamente las acciones extras para cada fila de la tabla.

        Override este método para agregar lógica condicional o usar self.

        Returns:
            list: Lista de diccionarios con acciones por fila

        Example:
            You can override this method to build row-level actions dynamically:

        ```python
        def get_extra_actions(self):
            actions = []

            # Lógica condicional basada en permisos
            if self.request.user.has_perm('app.special_permission'):
                actions.append({
                    "url": "app:special_action",
                    "params": {"pk": "pk"},
                    "icon": "fas fa-star",
                    "color": "text-warning",
                    "tooltip": "Acción especial",
                })

            # Acción común para todas las filas
            actions.append({
                "url": "app:common_action",
                "params": {"pk": "pk"},
                "icon": "fas fa-cog",
                "color": "text-primary",
                "tooltip": "Configurar",
                "validation": "can_configure",  # método de validación opcional
            })

            return actions
        ```

        These actions will be rendered as icon buttons in each row of the table,
        allowing users to perform actions on individual items.
        """
        return getattr(self, "extra_actions", [])

    def get_context_data(self, **kwargs) -> dict:
        """The function `get_context_data` in Python retrieves various context data for a view, such as fields, URLs, and other information.

        @return The `get_context_data` method is returning a dictionary `context` that contains various
        key-value pairs. The keys include "fields", "create_url", "edit_url", "delete_url",
        "detail_url", "return_url", "can_disable", "verbose_name", and "title". The values for these keys
        are obtained by calling different methods within the class.
        """
        context = super().get_context_data(**kwargs)

        context["fields"] = self.get_fields()
        context["field_attributes"] = self.get_field_attributes()
        context["create_url"] = self.get_create_url()
        context["edit_url"] = self.get_edit_url()
        context["delete_url"] = self.get_delete_url()
        context["detail_url"] = self.get_detail_url()
        context["return_url"] = self.get_return_url()
        context["disable_url"] = self.get_disable_url()
        context["can_disable"] = self.can_disable
        context["is_disabled_view"] = self.get_is_disabled_view()

        context["verbose_name"] = self.get_verbose_name()
        context["title"] = self.get_title()

        context["permissions"] = self.get_permissions()
        context["extra_actions"] = self.get_extra_actions()
        context["general_extra_actions"] = self.get_general_extra_actions()

        return context

    def get_queryset(self):
        """The function `get_queryset` returns a queryset based on a condition.

        @return The `queryset` variable is being returned.
        """
        queryset = super().get_queryset()
        if self.get_is_disabled_view():
            queryset = self.model.deleted_objects.all()
            return queryset

        if self.can_disable:
            queryset = self.model.all_objects.all()
        return queryset

    def get_paginated_queryset(self):
        """The function `get_paginated_queryset` retrieves a paginated queryset based on the request parameters.

        @return The `get_paginated_queryset` method returns a paginated queryset based on the current
        page number specified in the request. If the page number is not valid (e.g., not an integer), it
        defaults to the first page. If the page number exceeds the total number of pages, it redirects
        to the last valid page.
        """
        queryset = self.get_queryset()
        paginator = self.get_paginator(queryset, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            paginated_queryset = paginator.get_page(page)
        except PageNotAnInteger:
            paginated_queryset = paginator.get_page(1)
        except EmptyPage:
            # Redirect to the last valid page
            last_page = paginator.num_pages
            return redirect(f"{self.request.path}?page={last_page}")
        return paginated_queryset

    def get(self, request, *args, **kwargs):
        """The function retrieves a paginated list of objects and handles exceptions for invalid page numbers.

        @param request The `request` parameter in the `get` method is an HttpRequest object that
        represents the HTTP request made by the client to the server. It contains information about the
        request, such as the request method, headers, body, and query parameters. In the provided code
        snippet, the `request` parameter

        @return The `get` method is returning the response from the base implementation of the `get`
        method with the provided `request`, `args`, and `kwargs`.
        """
        # Call the base implementation first to get a context
        self.object_list = self.get_queryset()

        # Apply pagination
        paginator = self.get_paginator(self.object_list, self.paginate_by)
        page_number = request.GET.get("page")

        try:
            paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), redirect to the last page
            query_params = request.GET.copy()
            query_params["page"] = paginator.num_pages
            return redirect(f"{self.request.path}?{urlencode(query_params)}")

        return super().get(request, *args, **kwargs)


class GenericDeleteView(SuccessMessageMixin, generic.DeleteView):
    """Base class for DeleteView with additional functionality.

    Attributes:
        model (Model): Django model class to work with
        success_url (str): URL to redirect after successful deletion
        success_message (str): Message to display after successful deletion
        verbose_name (str): Custom verbose name for the model
        can_disable (bool): Flag to indicate if objects can be disabled instead of deleted
        is_htmx (bool): Flag to indicate if the request is an HTMX request
        is_delete (bool): Flag to indicate if the action is a delete or undelete operation

    Note:
        This class inherits from SuccessMessageMixin and generic.DeleteView.
        It provides additional functionality for handling both deletion and disabling of objects.
    """

    model = None
    success_url: str = None
    success_message: str = SUCCESS_ITEM_ACTION
    verbose_name: str = None
    is_htmx = False
    is_delete = None
    action_deleted = ACTION_DELETED_LABEL
    action_enabled = ACTION_RESTORED_LABEL
    can_disable = False

    def get_success_url(self):
        """Obtiene la URL de éxito incluyendo parámetros de consulta."""
        # Get all parameters from the request and concatenate them to the success_url
        url = super().get_success_url()
        params = self.request.GET.urlencode()
        if params:
            url = f"{url}?{params}"
        return url

    def get_success_message(self) -> str:
        """The function `get_success_message` returns a success message for a created object using a template string.

        @return The code is returning a success message string.
        """
        return self.success_message

    def get_verbose_name(self):
        """Obtiene el nombre verbose del modelo en minúsculas."""
        return self.model._meta.verbose_name.lower()

    def get_queryset(self):
        """Obtiene el queryset incluyendo objetos eliminados."""
        return self.model.all_objects.all()

    def post(self, request, *args, **kwargs):
        """Procesa la solicitud POST para eliminar o restaurar el objeto."""
        self.object = self.get_object()
        self.is_htmx = request.headers.get("HX-Request", False)
        self.is_delete = True if not self.object.deleted else False

        if self.is_delete:
            return self.delete(request, *args, **kwargs)

        if not self.can_disable:
            return self.handle_response(
                False,
                format_lazy(ERROR_DISABLE_ALREADY_DISABLED, object=self.object),
            )

        deleted, message = self.object.undelete()
        return self.handle_response(deleted, message)

    def delete(self, request, *args, **kwargs):
        """Elimina el objeto y redirige a la URL de éxito.

        Args:
            request: La solicitud HTTP.
            args: Argumentos posicionales adicionales.
            kwargs: Argumentos de palabra clave adicionales.

        Returns:
            Respuesta HTTP apropiada según el contexto.
        """
        self.object = self.get_object()
        deleted, message = self.object.delete()
        return self.handle_response(deleted, message)

    def handle_response(self, success, message):
        """Handle the response based on whether the operation was successful or not.

        For HTMX requests, return an appropriate message; for normal form submits, redirect.
        """
        success_url = self.get_success_url()

        if type(message) == str:
            messages.error(self.request, message)
            return self.get_response("ERROR", success_url)

        if not success:
            blocking_info = message.get("blocking_info", [])
            all_blocking_elements = []

            for info in blocking_info:
                app_label = info["app_label"]
                elements = info["elements"]
                model_str = info["model_str"]

                if not elements:
                    continue

                elements_ids = [element.id for element in elements]
                params = f"id={','.join(map(str, elements_ids))}"

                url_name = info.get("url_name")
                if not url_name:
                    url_name = f"{app_label}:index"

                try:
                    list_url = reverse(url_name)
                except NoReverseMatch:
                    list_url = "#"

                if list_url != "#":
                    list_url = f"{list_url}?{params}"

                link_html = format_html("<a href='{}'>{}</a>", list_url, model_str)
                all_blocking_elements.append(link_html)

            if len(all_blocking_elements) > 1:
                final_str = (
                    ", ".join(all_blocking_elements[:-1])
                    + " "
                    + LIST_CONJUNCTION_AND
                    + " "
                    + all_blocking_elements[-1]
                )
            else:
                final_str = ", ".join(all_blocking_elements)

            delete = message.get("delete")
            action = ACTION_DELETE_VERB if delete else ACTION_RESTORE_VERB
            final_message = format_html(
                ERROR_ACTION_BLOCKED,
                action=action,
                object=self.object,
                related=mark_safe(final_str),
            )

            messages.error(self.request, final_message)
            return self.get_response("ERROR", success_url)

        success_message = self.get_success_message()
        if success_message:
            action = self.action_deleted if self.is_delete else self.action_enabled
            messages.success(self.request, format_lazy(success_message, action=action))

        return self.get_response("OK", success_url)

    def get_response(self, htmx_message, redirect_url):
        """Return either an HttpResponse for HTMX requests or HttpResponseRedirect for normal form submissions."""
        if self.is_htmx:
            return HttpResponse(htmx_message)
        return HttpResponseRedirect(redirect_url)


class GenericCreateFormsetView(GenericCreateView):
    """GenericCreateFormsetView is a class-based view for creating multiple related objects in a single form.

    Attributes:
        `formset_config` (`List[Dict[str, Union[str, int, Any]]]`): A list of dictionaries containing formset configurations.
        `formset_classes` (`List[type[forms.BaseFormSet]]`): A list of formset classes.
        `template_name` (`str`): The template to render. Default is "generic/formset.html".

    Formset Configuration:
        The `formset_config` attribute is a list of dictionaries containing formset configurations. Each dictionary should contain the following keys:
        - `title` (`str`): The title of the formset.
        - `form` (`Form`): The form class to use for the formset. This class assumes that the form is a subclass of `forms.ModelForm`.
        - `prefix` (`str`): The prefix to use for the formset.
        - `related_name` (`str`): The related name that links the child model to the parent model.
        - `extra` (`int`, optional): The number of extra forms to display. Default is 1.
        - `base_formset` (`FormsetClass`, optional): The base formset class to use. Default is `GenericBaseFormSet`.

    Note:
        This class provides hooks to customize formset instance processing, formset instance saving, and formset kwargs. Those functions are:
        - `process_formset_instance`
        - `save_formset`
        - `get_formset_kwargs`

        This class also provides a hook to customize the main form instance before saving it. The function is:
        - `pre_save`

        Please refer to the documentation of each function for more information.
    """

    # formset_config = [
    #     {
    #         title : "Canciones",
    #         form : FormClass,
    #         prefix: "song",
    #         related_name: "album",
    #         # optional
    #         extra : int, # default 1
    #         base_formset : FormsetClass # default GenericBaseFormSet
    #     }
    # ]
    template_name = "generic/formset.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config: List[Dict[str, Union[str, int, Any]]] = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Handle POST request for formset creation."""
        self.object = None
        form = self.get_form()
        formsets = [
            formset_config.get("formset_class")(request.POST, **self.get_formset_kwargs(formset_config))
            for formset_config in self.get_formset_config()
        ]
        if form.is_valid() and all_valid(formsets):
            main_instance = self.pre_save(form)
            child_instances = {}
            main_instance.save()
            form.save_m2m()

            for formset_config, formset in zip(self.get_formset_config(), formsets):
                instances = []
                for child_form in formset:
                    child_form_instance = child_form.save(commit=False)
                    child_form_instance = self.process_formset_instance(
                        child_form_instance, formset_config, main_instance
                    )

                    instances.append(child_form_instance)

                child_objs = self.save_formset(formset_config, instances)

                for child_form in formset:
                    child_form.save_m2m()

                child_instances.update({formset_config.get("prefix"): child_objs})

            main_instance = self.post_save(main_instance, child_instances)

            if self.get_success_message(cleaned_data=form.cleaned_data):
                messages.success(self.request, self.get_success_message(form.cleaned_data))
            return redirect(self.get_success_url())

        context = self.get_context_data()
        context["form"] = form
        context["formsets"] = [
            (formset_config, formset_instance)
            for formset_config, formset_instance in zip(self.get_formset_config(), formsets)
        ]
        return self.render_to_response(context)

    def get_formset_kwargs(self, formset_config: Dict[str, Union[str, int, Any]]) -> Dict:
        """Hook to customize kwargs passed to formset instantiation.

        Args:
            formset_config (Dict[str, Union[str, int, Any]]): A dictionary containing formset configuration.

        Returns:
            Dict: A dictionary containing formset kwargs.

        Example:
            If you want to customize the formset kwargs, you can override this method.
        ```python
        def get_formset_kwargs(self, formset_config: Dict[str, Union[str, int, Any]]) -> Dict:
            kwargs = super().get_formset_kwargs(formset_config)
            kwargs.update({
                # custom logic here...
            })
            # or custom logic for an individual formset
            if formset_config.get("prefix") == "song":
                kwargs.update({
                    # custom logic here...
                })
            return kwargs
        """
        return {
            "prefix": formset_config.get("prefix"),
            "form_kwargs": {"user": self.request.user},
        }

    def create_formset_class(self, formset_config: Dict[str, Union[str, int, Any]]) -> type[forms.BaseFormSet]:
        """Create a formset class based on a formset configuration.

        Args:
            formset_config (Dict[str, Union[str, int, Any]]): A dictionary containing formset configuration.

        Returns:
            type[forms.BaseFormSet]: A formset class.
        """
        base_formset_class = formset_config.get("base_formset", GenericBaseFormSet)
        extra = formset_config.get("extra", 1)
        form = formset_config["form"]
        return formset_factory(form, base_formset_class, extra=extra)

    def process_formset_instance(self, child_form_instance: Any, formset_config: Dict, main_instance: Any) -> Any:
        """Hook to customize processing of individual formset instances before saving.

        Args:
            child_form_instance (Any): The formset instance to process.
            formset_config (Dict): The formset configuration.
            main_instance (Any): The main instance associated with the formset.

        Returns:
            Any: The processed formset instance.

        Example:
            If you want to set the related_name field of the child form instance, you can override this method as follows:

        ```python
        def process_formset_instance(self, child_form_instance: Any, formset_config: Dict, main_instance: Any) -> Any:
            child_form_instance = super().process_formset_instance(child_form_instance, formset_config, main_instance) # already assigns the parent instance to the related_name field
            # Identify the formset instance by the prefix
            if formset_config.get("prefix") == "song":
                # custom logic for instances of a single formset
            return child_form_instance
        """
        related_name = formset_config.get("related_name")
        setattr(child_form_instance, related_name, main_instance)

        return child_form_instance

    def post_save(self, main_instance: Any, instances: dict) -> Any:
        """Hook called after saving the main form instance.

        Args:
            main_instance (Any): The main form instance that was saved.
            instances (dict): A dictionary containing formset instances. Key is the formset prefix and value is a list of instances.

        Returns:
            Any: The main form instance.

        Example:
            If you want to do something after saving the main form instance, you can override this method as follows:

        ```python
        def post_save(self, main_instance: Any, instances: dict) -> Any:
            custom logic... # to do something after saving

            return main_instance
        ```
        """
        return main_instance

    def pre_save(self, form: forms.Form) -> Any:
        """Hook called before saving the main form instance.

        Args:
            form (forms.Form): The main form to process.

        Returns:
            Any: The processed main form instance.

        Example:
            If you want to set the created_by field of the main form instance, you can override this method as follows:

        ```python
        def pre_save(self, form: forms.Form) -> Any:
            instance = super().pre_save(form) # to call the default logic, this already assigns the created_by field
            custom logic... # to do something with the instance before saving
            return instance
        ```
        """
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        return instance

    def save_formset(self, formset_config: Dict[str, Union[str, int, Any]], instances: List[Any]) -> None:
        """Hook to customize how formset instances are saved to the database.

        Args:
            formset_config (Dict[str, Union[str, int, Any]]): The formset configuration.
            instances (List[Any]): A list of formset instances.

        Returns:
            None

        Example:
            If you want to save the instances using bulk_create, you can override this method as follows:

        ```python
        def save_formset(self, formset_config: Dict[str, Union[str, int, Any]], instances: List[Any]) -> None:
            custom logic... # to do something with the instances before saving

            # Identify an specific formset by the prefix
            if formset_config.get("prefix") == "song":
                custom logic... # to do something with the instances before saving

            super().save_formset(formset_config, instances) # to save the instances using the default logic
        ```
        """
        model = formset_config["form"].Meta.model
        child_objs = bulk_create_with_history(
            instances,
            model,
        )
        return child_objs

    def get_fields_titles(self, form_class: type[forms.Form]) -> str:
        """Get the field titles for a form class.

        Args:
            form_class (type[forms.Form]): The form class to get the field titles from.

        Returns:
            str: A list of field titles.
        """
        return [field.label or field.widget.attrs.get("placeholder") for field in form_class().fields.values()]

    def get_success_url(self) -> str:
        """Get the success URL for the view.

        Raises:
            ValueError: If the success_url attribute is not set.

        Returns:
            str: The success URL for the view.
        """
        if not self.success_url:
            raise ValueError("You must set a success_url attribute")
        return self.success_url

    def get_formset_config(self) -> List[Dict[str, Union[str, int, Any]]]:
        """Get the formset configuration for the view.

        Raises:
            `ValueError`: If the formset configuration is missing a required attribute. Required attributes are "prefix", "related_name", and "form".

        Returns:
            `List[Dict[str, Union[str, int, Any]]]`: A list of dictionaries containing formset configurations.
        """
        conflicts = []
        for formset_config in self.formset_config:
            prefix = formset_config.get("prefix")
            form_class = formset_config.get("form")

            form_fields = form_class().fields.keys()
            if prefix in form_fields:
                conflicts.append(prefix)

            if not formset_config.get("prefix"):
                raise ValueError("You must set a prefix attribute in formset_config")
            if not formset_config.get("related_name"):
                raise ValueError("You must set a related_name attribute in formset_config")
            if not formset_config.get("form"):
                raise ValueError("You must set a form attribute in formset_config")
            if formset_config.get("oneToNFormsets", None) == None:
                formset_config["oneToNFormsets"] = True

        if conflicts and hasattr(self, "request"):
            # NOT REMOVE: This is a feature to avoid proplems with automatization, if you remove this raise, there will be consequences
            raise ValueError(
                f"Formset prefix '{conflicts[0]}' conflicts with a field name in its associated form. Please choose a different prefix to avoid frontend rendering issues."
            )

        return self.formset_config

    def get_context_data(self, **kwargs) -> dict:
        """The function `get_context_data` adds additional context data to a dictionary and returns it.

        @return The `get_context_data` method is returning a dictionary `context` that contains the
        following key-value pairs:
        - "verbose_name": the result of calling the `get_verbose_name` method on `self`
        - "return_url": the result of calling the `get_return_url` method on `self`
        - "title": the result of calling the `get_title` method on `self`
        - "formsets": a list of tuples containing formset configurations and instances
        """
        context = super().get_context_data(**kwargs)
        context["formsets"] = [
            (formset_config, formset_config.get("formset_class")(prefix=formset_config.get("prefix")))
            for formset_config in self.get_formset_config()
        ]
        return context

    def create_formset_classes(self):
        """Create formset classes based on the formset configurations."""
        for formset_config in self.get_formset_config():
            formset_class = self.create_formset_class(formset_config)
            formset_config.update(
                {
                    "field_titles": self.get_fields_titles(formset_config.get("form")) + [FIELD_DISABLE_LABEL],
                    "formset_class": formset_class,
                }
            )


class GenericEditFormsetView(GenericUpdateView):
    """GenericEditFormsetView is a class-based view for editing multiple related objects in a single form.

    Attributes:
        `formset_config` (`List[Dict[str, Union[str, int, bool, Any]]]`): A list of dictionaries containing formset configurations.
        `formset_classes` (`List[type[forms.BaseFormSet]]`): A list of formset classes.
        `template_name` (`str`): The template to render the formset, default is "generic/formset.html".

    Formset Configuration:
        The `formset_config` attribute is a list of dictionaries containing formset configurations. Each dictionary should contain the following keys:
        - `title` (`str`): The title of the formset.
        - `parent` (`Model`): The parent model class.
        - `child` (`Model`): The child model class.
        - `form` (`Form`): The form class to use for the formset. This class assumes that the form is a subclass of `forms.ModelForm`.
        - `prefix` (`str`): The prefix to use for the formset.
        - `related_name` (`str`): The related name that links the child model to the parent model.
        - `extra` (`int`, optional): The number of extra forms to display. Default is 0.
        - `inline_formset` (`FormsetClass`, optional): The base formset class to use. Default is `GenericBaseInlineFormSet`.
        - `can_delete` (`bool`, optional): Whether the formset should allow deletion of instances. Default is False.

    Note:
        This class provides hooks to customize formset instance processing, formset instance saving, and formset kwargs. Those functions are:
        - `process_formset_instance`
        - `save_formset`
        - `get_formset_kwargs`

        This class also provides a hook to customize the main form instance before saving it. The function is:
        - `pre_save`

        Please refer to the documentation of each function for more information.
    """

    # formset_config = [
    #   {
    #      title : str,
    #      parent: ModelClass,
    #      child: ModelClass,
    #      form : FormClass,
    #      prefix: str,
    #      related_name: str,
    #      #optional,
    #      extra : int,
    #      inline_formset : FormsetClass,
    #      can_delete=False
    #   }
    # ]
    template_name = "generic/formset.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config: List[Dict[str, Union[str, int, bool, Any]]] = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Handle POST request for formset update."""
        self.object = self.get_object()
        user = request.user
        form = self.form_class(request.POST, request.FILES, instance=self.object, user=user)
        formsets = [
            formset_config.get("formset_class")(request.POST, **self.get_formset_kwargs(formset_config))
            for formset_config in self.get_formset_config()
        ]

        if form.is_valid() and all_valid(formsets):
            main_instance = self.pre_save(form)
            main_instance.save()
            form.save_m2m()
            new_child_instances = {}
            edited_child_instances = {}

            for formset_config, formset in zip(self.get_formset_config(), formsets):
                child_instances = []
                new_instances = []
                ids_inside_post = get_records_formset_by_prefix(request, formset.prefix)

                formset_config.get("child").objects.filter(
                    **{formset_config.get("related_name"): main_instance}
                ).exclude(id__in=ids_inside_post).delete()

                for child_form in formset:
                    child_form_instance = child_form.save(commit=False)

                    child_form_instance = self.process_formset_instance(
                        child_form_instance, formset_config, main_instance
                    )

                    if child_form_instance.pk:
                        child_instances.append(child_form_instance)
                        continue

                    new_instances.append(child_form_instance)

                new_objs, child_instances = self.save_formset(formset_config, new_instances, child_instances)

                for child_form in formset:
                    child_form.save_m2m()

                new_child_instances.update({formset_config.get("prefix"): new_objs})
                edited_child_instances.update({formset_config.get("prefix"): child_instances})

            main_instance = self.post_save(main_instance, new_child_instances, edited_child_instances)

            if self.get_success_message(cleaned_data=form.cleaned_data):
                messages.success(self.request, self.get_success_message(form.cleaned_data))
            return redirect(self.get_success_url())

        context = self.get_context_data()
        context["form"] = form
        context["formsets"] = [
            (formset_config, formset_instance)
            for formset_config, formset_instance in zip(self.get_formset_config(), formsets)
        ]
        return self.render_to_response(context)

    def pre_save(self, form: forms.Form) -> Any:
        """Hook called before saving the main form instance.

        Args:
            form (forms.Form): The main form to process.

        Returns:
            Any: The processed main form instance.

        Example:
        If you want to customize the main form instance before saving, you can override this method.
        ```python
        def pre_save(self, form: forms.Form) -> Any:
            instance = super().pre_save(form) # already assign the updated_by field
            # custom logic here...
            return instance
        ```
        """
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        return instance

    def post_save(self, main_instance: Any, new_instances: dict, edited_instances: dict) -> Any:
        """Hook called after saving the main form instance.

        Args:
            main_instance (Any): The main form instance that was saved.
            new_instances (dict): A dictionary containing new formset instances. Key is the formset prefix and value is a list of instances.
            edited_instances (dict): A dictionary containing edited formset instances. Key is the formset prefix and value is a list of instances.

        Returns:
            Any: The main form instance.

        Example:
        If you want to do something after saving the main form instance, you can override this method.
        ```python
        def post_save(self, main_instance: Any, new_instances: dict, edited_instances) -> Any:
            # custom logic here...
            return main_instance
        ```
        """
        return main_instance

    def get_formset_kwargs(self, formset_config: Dict[str, Union[str, int, bool, Any]]) -> Dict:
        """Hook to customize kwargs passed to formset instantiation.

        Args:
            formset_config (Dict[str, Union[str, int, bool, Any]]): A dictionary containing formset configuration.

        Returns:
            Dict: A dictionary containing formset kwargs.

        Example:
            If you want to customize the formset kwargs, you can override this method.
        ```python
        def get_formset_kwargs(self, formset_config: Dict[str, Union[str, int, Any]]) -> Dict:
            kwargs = super().get_formset_kwargs(formset_config)
            kwargs.update({
                # custom logic here...
            })
            # or custom logic for an individual formset
            if formset_config.get("prefix") == "song":
                kwargs.update({
                    # custom logic here...
                })
            return kwargs
        ```
        """
        return {
            "prefix": formset_config.get("prefix"),
            "instance": self.get_object(),
            "form_kwargs": {"user": self.request.user},
        }

    def process_formset_instance(
        self,
        child_form_instance: Any,
        formset_config: Dict[str, Union[str, int, bool, Any]],
        main_instance: Any,
    ) -> Any:
        """Hook to customize processing of individual formset instances before saving.

        Args:
            child_form_instance (Any): The formset instance to process.
            formset_config (Dict[str, Union[str, int, bool, Any]]): The formset configuration.
            main_instance (Any): The main instance associated with the formset.

        Returns:
            Any: The processed formset instance.

        Example:
            If you want to add custom logic to the child form instance before saving, you can override this method.
        ```python
        def process_formset_instance(self, child_form_instance: Any, formset_config: Dict[str, Union[str, int, bool, Any]], main_instance: Any) -> Any:
            child_form_instance = super().process_formset_instance(child_form_instance, formset_config, main_instance) # already assigns the parent instance to the related_name field

            # Identify the formset by the prefix
            if formset_config.get("prefix") == "song":
                # custom logic here...
                return child_form_instance

            return child_form_instance
        ```
        """
        related_name = formset_config.get("related_name")
        setattr(child_form_instance, related_name, main_instance)

        return child_form_instance

    def save_formset(
        self,
        formset_config: Dict[str, Union[str, int, bool, Any]],
        new_instances: List[Any],
        instances: List[Any],
    ) -> Tuple:
        """Hook to customize how formset instances are saved to the database.

        Args:
            formset_config (Dict[str, Union[str, int, bool, Any]]): The formset configuration.
            new_instances (List[Any]): A list of new model instances.
            instances (List[Any]): A list of already created model instances.

        Returns:
            Tuple: A tuple of the newly created child objects and the updated instances.

        Example:
            If you want to customize how formset instances are saved to the database, you can override this method.
        ```python
        def save_formset(self, formset_config: Dict[str, Union[str, int, bool, Any]], new_instances: List[Any], instances: List[Any]) -> None:
            # Identify the formset by the prefix
            if formset_config.get("prefix") == "song":
                # custom logic here...

            return super().save_formset(formset_config, new_instances, instances)
        ```
        """
        model = formset_config["form"].Meta.model
        new_child_objs = []

        if new_instances:
            new_child_objs = bulk_create_with_history(
                new_instances,
                model=model,
            )
        if instances:
            fields = [
                f.name
                for f in model._meta.get_fields()
                if f.name in formset_config["form"].Meta.fields and f.concrete and not isinstance(f, ManyToManyField)
            ]
            bulk_update_with_history(instances, model=model, fields=fields)

        return new_child_objs, instances

    def get_fields_titles(self, form_class: type[forms.Form]) -> str:
        """Get the titles of the fields in a form class.

        Args:
            form_class (type[forms.Form]): The form class to get the field titles from.

        Returns:
            List[str]: A list of field titles or placeholders from the form.
        """
        return [field.label or field.widget.attrs.get("placeholder") for field in form_class().fields.values()]

    def get_success_url(self) -> str:
        """Get the success URL for the view."""
        if not self.success_url:
            raise ValueError("You must set a success_url attribute")
        return self.success_url

    def get_formset_config(self) -> List[Dict[str, Union[str, int, bool, Any]]]:
        """Get the formset configuration for the view.

        Raises:
            ValueError: If any of the required attributes are missing in the formset configuration. Required attributes are "prefix", "related_name", "form", "parent", and "child".

        Returns:
            `List[Dict[str, Union[str, int, bool, Any]]]`: A list of dictionaries containing formset configurations.
        """
        conflicts = []
        for formset_config in self.formset_config:
            prefix = formset_config.get("prefix")
            form_class = formset_config.get("form")

            form_fields = form_class().fields.keys()
            if prefix in form_fields:
                conflicts.append(prefix)

            if not formset_config.get("prefix"):
                raise ValueError("You must set a prefix attribute in formset_config")
            if not formset_config.get("related_name"):
                raise ValueError("You must set a related_name attribute in formset_config")
            if not formset_config.get("form"):
                raise ValueError("You must set a form attribute in formset_config")
            if not formset_config.get("parent"):
                raise ValueError("You must set a parent attribute in formset_config")
            if not formset_config.get("child"):
                raise ValueError("You must set a child attribute in formset_config")

        if conflicts and hasattr(self, "request"):
            # NOT REMOVE: This is a feature to avoid proplems with automatization, if you remove this raise, there will be consequences
            raise ValueError(
                f"Formset prefix '{conflicts[0]}' conflicts with a field name in its associated form. Please choose a different prefix to avoid frontend rendering issues."
            )

        return self.formset_config

    def get_context_data(self, **kwargs) -> dict:
        """The function `get_context_data` adds additional context data to a dictionary and returns it.

        @return The `get_context_data` method is returning a dictionary `context` that contains the
        following key-value pairs:
        - "verbose_name": the result of calling the `get_verbose_name` method on `self`
        - "return_url": the result of calling the `get_return_url` method on `self`
        - "title": the result of calling the `get_title` method on `self`
        - "formsets": a list of tuples containing formset configurations and instances
        """
        context = super().get_context_data(**kwargs)
        context["formsets"] = [
            (
                formset_config,
                formset_config.get("formset_class")(prefix=formset_config.get("prefix"), instance=self.get_object()),
            )
            for formset_config in self.get_formset_config()
        ]
        return context

    def create_formset_class(
        self, formset_config: Dict[str, Union[str, int, bool, Any]]
    ) -> type[forms.BaseInlineFormSet]:
        """Create a formset class based on a formset configuration.

        Args:
            formset_config (Dict[str, Union[str, int, bool, Any]]): A dictionary containing formset configuration.

        Returns:
            type[forms.BaseInlineFormSet]: A formset class.
        """
        base_formset_class = formset_config.get("inline_formset", GenericBaseInlineFormSet)
        extra = formset_config.get("extra", 0)
        form = formset_config["form"]
        return inlineformset_factory(
            formset_config.get("parent"),
            formset_config.get("child"),
            form=form,
            formset=base_formset_class,
            extra=extra,
            can_delete=formset_config.get("can_delete", False),
            fk_name=formset_config.get("fk_name", formset_config.get("related_name")),
        )

    def create_formset_classes(self):
        """Create formset classes based on formset configuration."""
        for formset_config in self.get_formset_config():
            formset_class = self.create_formset_class(formset_config)
            formset_config.update(
                {
                    "field_titles": self.get_fields_titles(formset_config.get("form")) + [FIELD_DISABLE_LABEL],
                    "formset_class": formset_class,
                }
            )


class MultiParentFormsetView(GenericFormView, generic.FormView):
    """GenericEditFormsetView is a class-based view for editing multiple related objects in a single form.

    Attributes:
        `formset_config` (`List[Dict[str, Union[str, int, bool, Any]]]`): A list of dictionaries containing formset configurations.
        `formset_classes` (`List[type[forms.BaseFormSet]]`): A list of formset classes.
        `template_name` (`str`): The template to render the formset, default is "generic/formset.html".
        `parent_queryset` (`Iterable[Any]`): A queryset of parent instances, used to generate the formset_classes.

    Formset Configuration:
        The `formset_config` attribute is a list of dictionaries containing formset configurations. Each dictionary should contain the following keys:
        - `title` (`str`): The title of the formset.
        - `parent` (`Model`): The parent model class.
        - `child` (`Model`): The child model class.
        - `form` (`Form`): The form class to use for the formset. This class assumes that the form is a subclass of `forms.ModelForm`.
        - `prefix` (`str`): The prefix to use for the formset.
        - `related_name` (`str`): The related name that links the child model to the parent model.
        - `extra` (`int`, optional): The number of extra forms to display. Default is 0.
        - `inline_formset` (`FormsetClass`, optional): The base formset class to use. Default is `GenericBaseInlineFormSet`.
        - `can_delete` (`bool`, optional): Whether the formset should allow deletion of instances. Default is False.

    Note:
        This class provides hooks to customize formset instance processing, formset instance saving, and formset kwargs. Those functions are:
        - `process_formset_instance`
        - `save_formset`
        - `get_formset_kwargs`

        This class also provides a hook to customize the main form instance before saving it. The function is:
        - `pre_save`

        Please refer to the documentation of each function for more information.
    """

    template_name = "generic/multiparent_formset.html"
    form_class = EmptyForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formset_config: List[Dict[str, Union[str, int, bool, Any]]] = []
        self.parent_queryset: Iterable[Any] = None

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Handle POST request for multi-parent formset."""
        context = self.get_context_data()
        # form = self.form_class(request.POST, **self.get_form_kwargs())
        form = self.get_form()
        formsets = self.get_post_formsets(request=request)

        if not all_valid([formset[1] for formset in formsets]):
            context["form"] = form
            context["formsets"] = formsets
            return self.render_to_response(context)

        for formset_config, formset in formsets:
            parent_instance = formset.instance
            child_instances = []
            new_instances = []
            ids_inside_post = get_records_formset_by_prefix(request, formset.prefix)

            formset_config.get("child").objects.filter(
                **{formset_config.get("related_name"): parent_instance}
            ).exclude(id__in=ids_inside_post).delete()

            for child_form in formset:
                child_form_instance = child_form.save(commit=False)

                child_form_instance = self.process_formset_instance(
                    child_form_instance, formset_config, parent_instance
                )

                if child_form_instance.pk:
                    child_instances.append(child_form_instance)
                    continue

                new_instances.append(child_form_instance)

            new_objs, child_instances = self.save_formset(formset_config, new_instances, child_instances)

            for child_form in formset:
                child_form.save_m2m()

        if self.get_success_message(cleaned_data={}):
            messages.success(self.request, self.get_success_message({}))
        return redirect(self.get_success_url())

    def get_formset_kwargs(
        self, formset_config: Dict[str, Union[str, int, bool, Any]], parent_instance: Any, index: int
    ) -> Dict:
        """Hook to customize kwargs passed to formset instantiation.

        Args:
            formset_config (Dict[str, Union[str, int, bool, Any]]): A dictionary containing formset configuration.
            parent_instance (Any): The parent instance for the formset.
            index (int): The index of the parent instance.

        Returns:
            Dict: A dictionary containing formset kwargs.

        Example:
            If you want to customize the formset kwargs, you can override this method.
        ```python
        def get_formset_kwargs(self, formset_config: Dict[str, Union[str, int, Any]]) -> Dict:
            kwargs = super().get_formset_kwargs(formset_config)
            kwargs.update({
                # custom logic here...
            })
            # or custom logic for an individual formset
            if formset_config.get("prefix") == "song":
                kwargs.update({
                    # custom logic here...
                })
            return kwargs
        ```
        """
        return {
            "prefix": f"{formset_config.get('prefix')}_{index}",
            "form_kwargs": {"user": self.request.user},
        }

    def process_formset_instance(
        self,
        child_form_instance: Any,
        formset_config: Dict[str, Union[str, int, bool, Any]],
        main_instance: Any,
    ) -> Any:
        """Hook to customize processing of individual formset instances before saving.

        Args:
            child_form_instance (Any): The formset instance to process.
            formset_config (Dict[str, Union[str, int, bool, Any]]): The formset configuration.
            main_instance (Any): The main instance associated with the formset.

        Returns:
            Any: The processed formset instance.

        Example:
            If you want to add custom logic to the child form instance before saving, you can override this method.
        ```python
        def process_formset_instance(self, child_form_instance: Any, formset_config: Dict[str, Union[str, int, bool, Any]], main_instance: Any) -> Any:
            child_form_instance = super().process_formset_instance(child_form_instance, formset_config, main_instance) # already assigns the parent instance to the related_name field

            # Identify the formset by the prefix
            if formset_config.get("prefix") == "song":
                # custom logic here...
                return child_form_instance

            return child_form_instance
        ```
        """
        related_name = formset_config.get("related_name")
        setattr(child_form_instance, related_name, main_instance)

        return child_form_instance

    def save_formset(
        self,
        formset_config: Dict[str, Union[str, int, bool, Any]],
        new_instances: List[Any],
        instances: List[Any],
    ) -> Tuple:
        """Hook to customize how formset instances are saved to the database.

        Args:
            formset_config (Dict[str, Union[str, int, bool, Any]]): The formset configuration.
            new_instances (List[Any]): A list of new model instances.
            instances (List[Any]): A list of already created model instances.

        Returns:
            Tuple: A tuple of the newly create child objects and the updated instances.

        Example:
            If you want to customize how formset instances are saved to the database, you can override this method.
        ```python
        def save_formset(self, formset_config: Dict[str, Union[str, int, bool, Any]], new_instances: List[Any], instances: List[Any]) -> None:
            # Identify the formset by the prefix
            if formset_config.get("prefix") == "song":
                # custom logic here...

            return super().save_formset(formset_config, new_instances, instances)
        ```
        """
        model = formset_config["form"].Meta.model
        new_child_objs = []

        if new_instances:
            new_child_objs = bulk_create_with_history(
                new_instances,
                model=model,
            )
        if instances:
            fields = [
                f.name
                for f in model._meta.get_fields()
                if f.name in formset_config["form"].Meta.fields and f.concrete and not isinstance(f, ManyToManyField)
            ]
            bulk_update_with_history(instances, model=model, fields=fields)

        return new_child_objs, instances

    def get_post_formsets(self, request) -> List[Tuple[Dict, forms.BaseInlineFormSet]]:
        """Method to get the formsets info from the POST request.

        Args:
            request: POST request

        Returns:
            List[forms.BaseInlineFormSet]: List of formsets from the post request.
        """
        formsets = []

        for formset_config in self.get_formset_config():
            for index, parent_instance in enumerate(self.get_parent_queryset()):
                # Create copy to assign unique titles to each formset
                formset_config_copy = formset_config.copy()
                formset_class = formset_config_copy.get("formset_class")
                formset_config_copy.update(
                    {
                        "title": self.get_formset_title(
                            parent_instance=parent_instance, prefix=formset_config_copy.get("prefix")
                        )
                        or formset_config_copy.get("title")
                    }
                )
                kwargs: Dict = self.get_formset_kwargs(formset_config, parent_instance, index)
                kwargs.update({"instance": parent_instance})
                formset_instance = formset_class(request.POST, **kwargs)
                formsets.append((formset_config_copy, formset_instance))

        return formsets

    def get_formsets(self) -> List[Tuple]:
        """Method to get all formsets, for each parent object.

        Assigns the prefix based on the parent object primary key.

        Returns:
            List[Tuple]: Formset configs along with the formset instances.
        """
        formsets = []
        for formset_config in self.get_formset_config():
            for index, parent_instance in enumerate(self.get_parent_queryset()):
                # Create copy to assign unique titles to each formset
                formset_config_copy = formset_config.copy()
                formset_class = formset_config_copy.get("formset_class")
                formset_config_copy.update(
                    {
                        "title": self.get_formset_title(
                            parent_instance=parent_instance, prefix=formset_config_copy.get("prefix")
                        )
                        or formset_config_copy.get("title")
                    }
                )
                formsets.append(
                    (
                        formset_config_copy,
                        formset_class(
                            prefix=f"{formset_config.get('prefix')}_{index}",
                            instance=parent_instance,
                        ),
                    )
                )

        return formsets

    def get_fields_titles(self, form_class: type[forms.Form]) -> str:
        """Get the titles of the fields in a form class.

        Args:
            form_class (type[forms.Form]): The form class to get the field titles from.

        Returns:
            List[str]: A list of field titles or placeholders from the form.
        """
        return [field.label or field.widget.attrs.get("placeholder") for field in form_class().fields.values()]

    def get_success_url(self) -> str:
        """Get the success URL for the view."""
        if not self.success_url:
            raise NotImplementedError("You must set a success_url attribute")
        return self.success_url

    def get_formset_config(self) -> List[Dict[str, Union[str, int, bool, Any]]]:
        """Get the formset configuration for the view.

        Raises:
            ValueError: If any of the required attributes are missing in the formset configuration. Required attributes are "prefix", "related_name", "form", "parent", and "child".

        Returns:
            `List[Dict[str, Union[str, int, bool, Any]]]`: A list of dictionaries containing formset configurations.
        """
        for formset_config in self.formset_config:
            if not formset_config.get("prefix"):
                raise ValueError("You must set a prefix attribute in formset_config")
            if not formset_config.get("related_name"):
                raise ValueError("You must set a related_name attribute in formset_config")
            if not formset_config.get("form"):
                raise ValueError("You must set a form attribute in formset_config")
            if not formset_config.get("parent"):
                raise ValueError("You must set a parent attribute in formset_config")
            if not formset_config.get("child"):
                raise ValueError("You must set a child attribute in formset_config")
        return self.formset_config

    def get_context_data(self, **kwargs) -> dict:
        """The function `get_context_data` adds additional context data to a dictionary and returns it.

        Returns:
            The `get_context_data` method is returning a dictionary `context` that contains the
            following key-value pairs:
            - "verbose_name": the result of calling the `get_verbose_name` method on `self`
            - "return_url": the result of calling the `get_return_url` method on `self`
            - "title": the result of calling the `get_title` method on `self`
            - "formsets": a list of tuples containing formset configurations and instances
        """
        context = super().get_context_data(**kwargs)
        context["formsets"] = self.get_formsets()
        return context

    def get_formset_title(self, parent_instance: Any, prefix: str):
        """Method to get the title each formset will have.

        By default returns None and uses the title set in `formset_config`.

        Args:
            parent_instance (Any): The parent instance of the formset.
            prefix (str): The prefix assigned to the formset.

        Returns:
            str: The title that will appear on top of the formset.
        """
        return None

    def get_parent_queryset(self):
        """Method that returns the `parent_queryset` attribute.

        Raises:
            ValueError: Is `parent_queryset` isn't set at all.

        Returns:
            Iterable[type[BaseModel]]: The parent_queryset object.
        """
        if self.parent_queryset is None:
            self.set_parent_queryset()
            if self.parent_queryset is None:
                raise NotImplementedError("You must set the parent_queryset attribute")

        return self.parent_queryset

    def set_parent_queryset(self):
        """Method that sets the `parent_queryset` attribute for the class.

        This method must be implemented by the subclass.

        Raises:
            NotImplementedError: If the subclass didn't implement the method.
        """
        raise NotImplementedError("The subclass must implement the set_parent_queryset method")

    def create_formset_class(
        self, formset_config: Dict[str, Union[str, int, bool, Any]]
    ) -> type[forms.BaseInlineFormSet]:
        """Create a formset class based on a formset configuration.

        Args:
            formset_config (Dict[str, Union[str, int, bool, Any]]): A dictionary containing formset configuration.

        Returns:
            type[forms.BaseInlineFormSet]: A formset class.
        """
        base_formset_class = formset_config.get("inline_formset", GenericBaseInlineFormSet)
        extra = formset_config.get("extra", 0)
        form = formset_config["form"]
        return inlineformset_factory(
            formset_config.get("parent"),
            formset_config.get("child"),
            form=form,
            formset=base_formset_class,
            extra=extra,
            can_delete=formset_config.get("can_delete", False),
        )

    def create_formset_classes(self):
        """Method that creates the formset classes based on `formset_config`."""
        for formset_config in self.get_formset_config():
            formset_class = self.create_formset_class(formset_config)
            formset_config.update(
                {
                    "field_titles": self.get_fields_titles(formset_config.get("form")) + [FIELD_DISABLE_LABEL],
                    "formset_class": formset_class,
                }
            )


class GenericReportView(GenericFilterView):
    """Generic view for handling reports."""

    download_report_view: str = None
    send_report_view: str = None
    report_permission: str = None
    report_label: str = None
    send_report_label: str = None
    report_api_url = f"{settings.REPORTES_API_INTERNAL}/api/report"
    error_message = ERROR_REPORT_GENERATION

    def get_report_permission(self):
        """Get the report permission."""
        return self.report_permission or self.get_permission_required()

    def get_context_data(self, **kwargs):
        """Get context data for report view.

        Adds report-specific context variables.
        """
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "download_report_view": self.download_report_view,
                "send_report_view": self.send_report_view,
                "report_permission": self.get_report_permission(),
                "report_label": self.report_label,
                "send_report_label": self.send_report_label,
            }
        )
        return context

    def get_filters(self, request):
        """Get filters from request."""
        filterset_class = self.get_filterset_class()
        filters = {key: request.GET.get(key) for key in filterset_class.get_filters().keys() if request.GET.get(key)}
        filters["timezone"] = get_user_timezone(request)
        return filters

    def generate_report(self, request, *args, **kwargs):
        """Generate and return report."""
        if not self.has_permission():
            return self.handle_no_permission()

        response = send_get_request(self.report_api_url, self.get_token(), params=self.get_filters(request))
        return self.process_response(response)

    def send_report(self, request, *args, **kwargs):
        """Send report via email."""
        if not self.has_permission():
            return self.handle_no_permission()

        response = send_get_request(self.report_api_url, self.get_token(), params=self.get_filters(request))
        if response.status_code == 200:
            self.send_email_report(request.user, response)
            return JsonResponse({"message": SUCCESS_REPORT_SENT}, status=200)
        return self.handle_error()

    def send_email_report(self, user, response):
        """Send email with report attachment."""
        data = response.json()
        if "data" not in data:
            return JsonResponse({"error": ERROR_REPORT_NO_VALID_DATA}, status=400)

        context = {
            "email": user.email,
            "email_content": {
                "username": user.username,
                "url": f"{settings.SITIO}",
                "nombre": user.username,
            },
            "subject": REPORT_EMAIL_SUBJECT,
            "body_template": "email/reportes.html",
            "attachment_base64": data["data"],
            "file_name": REPORT_FILE_NAME,
        }
        async_task(self.send_email_credenciales, context)

    def send_email_credenciales(self, context):
        """Send email with credentials."""
        email_message = EmailMessage(
            context["subject"],
            self.render_email_body(context["body_template"], context["email_content"]),
            to=[context["email"]],
        )
        email_message.attach(
            context["file_name"],
            base64.b64decode(context["attachment_base64"]),
            "application/pdf",
        )
        email_message.content_subtype = "html"
        email_message.send()

    def render_email_body(self, template_name, context):
        """Render email body from template."""
        from django.template.loader import render_to_string

        return render_to_string(template_name, context)

    def handle_error(self):
        """Handle error response."""
        if settings.DEBUG:
            self.error_message += ERROR_REPORT_DEBUG_NO_RESPONSE
        return JsonResponse({"error": self.error_message}, status=400)

    def process_response(self, response):
        """Process API response."""
        try:
            data = response.json()
            if response.status_code == 200:
                return JsonResponse(data, status=200)
        except ValueError:
            pass
        return self.handle_error()
