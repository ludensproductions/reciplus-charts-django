import logging
from urllib.parse import urlencode

import httpx
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View, generic
from django.views.generic.edit import FormView
from django_select2.views import AutoResponseView
from simple_history.utils import bulk_create_with_history

from apps.comun.consts import SUCCESS_GROUPS_ASSIGNED
from apps.comun.mixins import EnsureDatabaseConnectionMixin
from apps.comun.views import (
    CustomLoginView,
    GenericCreateView,
    GenericDeleteView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.oauth2.const import (
    PROVIDER_PATH_LOGOUT,
    PROVIDER_PATH_REVOKE,
    SESSION_KEY_ACCESS_TOKEN,
    SESSION_KEY_ID_TOKEN,
    URL_OAUTH2_AUTHORIZE,
)

from .consts import (
    ADD_GROUP_PERMISSION,
    ADD_PERMISSION,
    BAN_PERMISSION,
    BAN_URL,
    CHANGE_PERMISSION,
    CREATE_TITLE,
    CREATE_URL,
    DELETE_PERMISSION,
    DELETE_URL,
    EDIT_TITLE,
    EDIT_URL,
    FILTER_FIELDS,
    FORGOT_PASSWORD_SUBTITLE,
    FORGOT_PASSWORD_SUCCESS_MESSAGE,
    FORGOT_PASSWORD_SUCCESS_TITLE,
    FORGOT_PASSWORD_TITLE,
    GROUPS_TITLE,
    GROUPS_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    ORDERING,
    PASSWORD_RESET_COMPLETE_MESSAGE,
    PASSWORD_RESET_COMPLETE_TITLE,
    PASSWORD_RESET_INVALID_LINK_MESSAGE,
    PASSWORD_RESET_INVALID_LINK_TITLE,
    PASSWORD_RESET_TITLE,
    PROFILE_SUCCESSFUL_UPDATE_MESSAGE,
    RETURN_URL,
    SUCCESS_USER_BANNED,
    SUCCESS_USER_UNBANNED,
    VIEW_PERMISSION,
)
from .forms import (
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    DomicilioForm,
    EditProfileForm,
    GroupsUserForm,
    NewUserForm,
    UserForm,
)
from .models import User, UserGroup
from .utils import generate_temporary_password, get_deleted_username_candidate, send_user_welcome_email

logger = logging.getLogger(__name__)


class RegisterView(generic.FormView):
    """Page for user self-registration.

    Allows new users to create an account by submitting a registration form.
    Upon successful registration, the user is logged in and redirected to home.
    """

    template_name = "registration/register.html"
    form_class = NewUserForm
    success_url = reverse_lazy("login")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Process user registration form and create account.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to home or re-rendered form with errors.
        """
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

        else:
            context = {"form": form}
            return render(request, self.template_name, context)


class NormalLoginView(EnsureDatabaseConnectionMixin, CustomLoginView):
    """Vista de inicio de sesión estándar (sin OAuth2)."""

    template_name = "registration/login.html"


class NormalLogoutView(View):
    """Cierra la sesión local y redirige al login."""

    def post(self, request, *args, **kwargs):
        """Handles POST logout."""
        logout(request)
        return redirect("/")

    def get(self, request, *args, **kwargs):
        """Handles GET logout."""
        logout(request)
        return redirect("/")


class LoginView(CustomLoginView):
    """Vista de inicio de sesión. Redirige al flujo OAuth2 del proveedor."""

    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        """Redirect unauthenticated users to the OAuth2 provider."""
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return redirect(reverse_lazy("oauth2:authorize"))

    def post(self, request, *args, **kwargs):
        """Block traditional login; redirect to OAuth2 provider."""
        return redirect(reverse_lazy("oauth2:authorize"))


class LogoutRedirectView(View):
    """Clears the local session, revokes token, and redirects to provider logout."""

    def post(self, request, *args, **kwargs):
        """Handles POST logout (from navbar form).

        Args:
            request: The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional positional and keyword arguments.

        Returns:
            HttpResponseRedirect: Redirect to the provider's logout URL.
        """
        return self._perform_logout(request)

    def get(self, request, *args, **kwargs):
        """Handles GET logout (direct URL access).

        Args:
            request: The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional positional and keyword arguments.

        Returns:
            HttpResponseRedirect: Redirect to the provider's logout URL.
        """
        return self._perform_logout(request)

    def _perform_logout(self, request):
        """Revokes token, clears local session, and redirects to provider logout.

        Args:
            request: The incoming HTTP request.

        Returns:
            HttpResponseRedirect: Redirect to provider logout or authorize URL.
        """
        access_token = request.session.get(SESSION_KEY_ACCESS_TOKEN, "")
        id_token = request.session.get(SESSION_KEY_ID_TOKEN, "")
        if access_token:
            self._revoke_token(access_token)
        logout(request)

        provider_url = settings.PROVIDER_URL_EXTERNAL
        redirect_uri_logout = settings.REDIRECT_URI_LOGOUT
        if provider_url and redirect_uri_logout:
            params = {"post_logout_redirect_uri": redirect_uri_logout}
            if id_token:
                params["id_token_hint"] = id_token
            return redirect(f"{provider_url}{PROVIDER_PATH_LOGOUT}?{urlencode(params)}")
        return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))

    def _revoke_token(self, access_token):
        """Revokes the access token on the OAuth2 provider.

        Args:
            access_token: The OAuth2 access token to revoke.
        """
        try:
            provider_url = settings.PROVIDER_URL_INTERNAL
            revoke_url = f"{provider_url}{PROVIDER_PATH_REVOKE}"
            data = {
                "token": access_token,
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            }
            with httpx.Client() as client:
                client.post(revoke_url, data=data)
        except Exception:
            logger.exception("Error revoking OAuth2 token on provider")


# Password Reset
class ForgotPasswordView(PasswordResetView):
    """Vista para solicitar recuperación de contraseña por correo."""

    template_name = "registration/forgot-password.html"
    form_class = CustomPasswordResetForm
    email_template_name = "registration/password_reset_email.html"
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

    def get_context_data(self, **kwargs):
        """Agrega textos de la vista al contexto."""
        context = super().get_context_data(**kwargs)
        context["title"] = FORGOT_PASSWORD_TITLE
        context["subtitle"] = FORGOT_PASSWORD_SUBTITLE
        return context


class PasswordResetDoneView(generic.TemplateView):
    """Vista de confirmación tras enviar el correo de recuperación."""

    template_name = "registration/password_reset_done.html"

    def get_context_data(self, **kwargs):
        """Agrega textos de la vista al contexto."""
        context = super().get_context_data(**kwargs)
        context["title"] = FORGOT_PASSWORD_SUCCESS_TITLE
        context["message"] = FORGOT_PASSWORD_SUCCESS_MESSAGE
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vista para establecer la nueva contraseña desde el enlace del correo."""

    template_name = "registration/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")

    def get_context_data(self, **kwargs):
        """Agrega textos de la vista al contexto."""
        context = super().get_context_data(**kwargs)
        context["title"] = PASSWORD_RESET_TITLE
        context["invalid_link_title"] = PASSWORD_RESET_INVALID_LINK_TITLE
        context["invalid_link_message"] = PASSWORD_RESET_INVALID_LINK_MESSAGE
        return context


class PasswordResetCompleteView(generic.TemplateView):
    """Vista de confirmación tras restablecer la contraseña exitosamente."""

    template_name = "registration/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        """Agrega textos de la vista al contexto."""
        context = super().get_context_data(**kwargs)
        context["title"] = PASSWORD_RESET_COMPLETE_TITLE
        context["message"] = PASSWORD_RESET_COMPLETE_MESSAGE
        return context


# Profile
class ProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """Page for authenticated user to edit their profile.

    Allows the logged-in user to update their profile information.
    """

    model = User
    template_name = "users/profile.html"
    form_class = EditProfileForm
    success_url = reverse_lazy("profile")  # Redirect to index after
    success_message = PROFILE_SUCCESSFUL_UPDATE_MESSAGE

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Process profile update form submission.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect after successful update or re-render with errors.
        """
        return super(ProfileView, self).post(request, *args, **kwargs)

    def get_object(self, **kwargs):
        """Retrieve the currently authenticated user.

        Returns:
            User: The authenticated user instance.
        """
        return self.request.user


class RegisterViewAdmin(generic.FormView):
    """Page for administrator to register new users.

    Allows an admin user to create new user accounts in the system.
    Newly created users are registered but not automatically logged in.
    """

    template_name = "registration/register.html"
    form_class = NewUserForm
    success_url = reverse_lazy("login")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Process user registration form via admin panel.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to home or re-rendered form with errors.
        """
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            form.save()
            # login(request, user)
            return redirect("/")

        else:
            context = {"form": form}
            return render(request, self.template_name, context)


class UserSelect2ResponseView(PermissionRequiredMixin, AutoResponseView):
    """API endpoint for Select2 autocomplete of users.

    Provides a RESTful interface to fetch user suggestions for Select2
    dropdown inputs with proper permission checks.
    """

    permission_required = VIEW_PERMISSION


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Page to list and filter users.

    Displays all non-deleted users with filtering and searching capabilities.
    Requires view_user permission.
    """

    permission_required = VIEW_PERMISSION
    model = User
    template_name = "users/index.html"
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING
    create_url = CREATE_URL
    delete_url = DELETE_URL
    edit_url = EDIT_URL
    return_url = RETURN_URL
    groups_url = GROUPS_URL
    ban_url = BAN_URL

    def get_context_data(self, **kwargs):
        """Add groups URL to template context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with added groups_url.
        """
        context = super().get_context_data(**kwargs)
        context["groups_url"] = self.groups_url
        context["ban_url"] = self.ban_url
        context["can_ban"] = self.request.user.has_perm(BAN_PERMISSION)
        return context

    def get_queryset(self):
        """Retrieve non-deleted users.

        Returns:
            QuerySet: Users with no soft-delete timestamp.
        """
        return super().get_queryset().filter(deleted__isnull=True)


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Page to create a new user.

    Displays a form to create a new user with optional address information.
    Requires add_user permission.
    """

    permission_required = ADD_PERMISSION
    model = User
    form_class = UserForm
    domicilio_form_class = DomicilioForm
    success_url = reverse_lazy(INDEX_URL)
    return_url = INDEX_URL
    title = CREATE_TITLE
    template_name = "users/form.html"

    def get_context_data(self, **kwargs):
        """Add address form to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with address form instance.
        """
        context = super().get_context_data(**kwargs)

        context["domicilio_form"] = DomicilioForm(prefix="domicilio")
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Process user creation form with optional address.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to user list or re-rendered form with errors.
        """
        self.object = None
        context = self.get_context_data(**kwargs)

        user_form = self.get_form()
        domicilio_form = self.domicilio_form_class(request.POST, prefix="domicilio")

        user_form_is_valid = user_form.is_valid()
        domicilio_form_is_valid = True  # Default to True if not needed

        has_domicilio = user_form.cleaned_data.get("has_domicile", False)

        if has_domicilio:
            domicilio_form_is_valid = domicilio_form.is_valid()

        if not user_form_is_valid or not domicilio_form_is_valid:
            context = self.get_context_data()
            context["form"] = user_form
            context["domicilio_form"] = domicilio_form

            return render(request, self.template_name, context)

        self.object = user_form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.username = user_form.cleaned_data["email"]
        temporary_password = generate_temporary_password()
        self.object.set_password(temporary_password)
        self.object.save()

        if has_domicilio:
            domicilio = domicilio_form.save(commit=False)
            domicilio.created_by = self.request.user
            domicilio.save()

            self.object.domicilio = domicilio

        self.object.save()
        send_user_welcome_email(self.object, temporary_password)
        messages.success(request, self.get_success_message(user_form.cleaned_data))
        return redirect(self.success_url)


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Page to edit an existing user.

    Allows updating user information and associated address details.
    Requires change_user permission.
    """

    permission_required = CHANGE_PERMISSION
    model = User
    form_class = UserForm
    domicilio_form_class = DomicilioForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL
    template_name = "users/form.html"

    def get_context_data(self, **kwargs):
        """Add address form to context with existing instance data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with address form instance.
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["domicilio_form"] = DomicilioForm(prefix="domicilio", instance=user.domicilio)

        if user.domicilio:
            context["has_domicilio"] = True

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Process user edit form with optional address update.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to user list or re-rendered form with errors.
        """
        self.object = None
        context = self.get_context_data(**kwargs)

        user_form = self.form_class(request.POST, instance=self.get_object())
        domicilio_form = self.domicilio_form_class(request.POST, prefix="domicilio")

        user_form_is_valid = user_form.is_valid()
        domicilio_form_is_valid = True  # Default to True if not needed

        has_domicilio = user_form.cleaned_data.get("has_domicile", False)

        if has_domicilio:
            domicilio_form_is_valid = domicilio_form.is_valid()

        if not user_form_is_valid or not domicilio_form_is_valid:
            context = self.get_context_data()
            context["form"] = user_form
            context["domicilio_form"] = domicilio_form

            return render(request, self.template_name, context)

        self.object = user_form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.username = user_form.cleaned_data["email"]

        if has_domicilio:
            domicilio = domicilio_form.save(commit=False)

            if not domicilio.pk:
                domicilio.created_by = self.request.user

            domicilio.updated_by = self.request.user
            domicilio.save()

            self.object.domicilio = domicilio

        elif not has_domicilio:
            domicilio = self.object.domicilio
            self.object.domicilio = None

            if domicilio:
                domicilio.delete()

        self.object.save()
        messages.success(request, self.success_message)
        return redirect(self.success_url)


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Page to delete a user.

    Soft-deletes a user record (marks as deleted without removing from DB).
    Requires delete_user permission.
    """

    permission_required = DELETE_PERMISSION
    model = User
    success_url = reverse_lazy(INDEX_URL)
    can_disable = False

    def delete(self, request, *args, **kwargs):
        """Rename username before soft-delete so the original value can be reused."""
        self.object = self.get_object()
        self.object.username = get_deleted_username_candidate(self.object.username)
        self.object.updated_by = request.user
        self.object.save(update_fields=["username", "updated_by", "updated_at"])
        return super().delete(request, *args, **kwargs)


class BanUserView(PermissionRequiredMixin, View):
    """Vista para banear/desbanear un usuario."""

    permission_required = BAN_PERMISSION

    def post(self, request, *args, **kwargs):
        """Alterna el estado de baneo del usuario."""
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.is_banned = not user.is_banned
        fields_to_update = ["is_banned"]

        if user.is_banned:
            user.force_logout_at = timezone.now()
            fields_to_update.append("force_logout_at")

        user.save(update_fields=fields_to_update)

        if user.is_banned:
            messages.success(request, SUCCESS_USER_BANNED)
        else:
            messages.success(request, SUCCESS_USER_UNBANNED)

        params = request.GET.urlencode()
        url = reverse_lazy(INDEX_URL)
        if params:
            url = f"{url}?{params}"
        return redirect(url)


# class DetailView(PermissionRequiredMixin, GenericMultiEntityDetailView):
#     permission_required = "users.view_departamento"
#     model = Departamento
#     context_object_name = "departamento"
#     return_url = "users:index"
#     title = "Detalles del departamento"

#     shown_fields = {
#         "nombre_departamento": "Nombre del departamento",
#         "departamento_superior": "Departamento superior",
#     }

#     children_entities = {
#         "puestos_departamentos": {"puesto": "Puesto", "jefe_departamento": "¿Es jefe de departamento?"},
#     }

#     table_title = {"puestos_departamentos": "Puestos"}


# class DisabledIndexView(PermissionRequiredMixin, GenericFilterView):
#     model = Departamento
#     permission_required = "users.enable_departamento"
#     title = "Inventario de departamentos deshabilitados"
#     ordering = ["-id"]
#     backward = "users:index"
#     is_disabled_view = True
#     queryset = Departamento.deleted_objects.all()

#     filter_fields = {
#         "nombre_departamento": {"label": "Departamento", "placeholder": "Departamento"},
#         "departamento_superior": {"label": "Departamento superior"},
#     }

#     shown_fields = {
#         "nombre_departamento": "Departamento",
#         "departamento_superior": "Departamento superior",
#     }

#     delete_url = "users:enable"
#     return_url = "users:index"


# class EnableView(PermissionRequiredMixin, GenericDeleteView):
#     permission_required = "users.delete_departamento"
#     model = Departamento
#     success_url = reverse_lazy("users:index")
#     success_message = "¡Elemento {action} exitosamente!"
#     can_disable = True
#     is_delete = False


class AddGroupView(PermissionRequiredMixin, FormView):
    """Page to manage group membership for a user.

    Allows assigning and removing groups (permission sets) for a specific user.
    Requires add_usergroup permission.
    """

    permission_required = ADD_GROUP_PERMISSION
    form_class = GroupsUserForm
    template_name = "generic/form.html"
    success_url = reverse_lazy(INDEX_URL)
    return_url = INDEX_URL
    title = GROUPS_TITLE
    success_message = SUCCESS_GROUPS_ASSIGNED

    def dispatch(self, request, *args, **kwargs):
        """Retrieve user instance before processing request.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments (must include "pk").

        Returns:
            HttpResponse: Rendered response or 404.

        Raises:
            Http404: If user with given pk does not exist.
        """
        self.user = get_object_or_404(User, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Initialize form with user's current group membership.

        Returns:
            dict: Dictionary with auth_group field populated with current groups.
        """
        current_groups = UserGroup.objects.filter(user=self.user).values_list("auth_group", flat=True)
        return {"auth_group": list(current_groups)}

    def get_context_data(self, **kwargs):
        """Add page title and return URL to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with title and return_url.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["return_url"] = self.return_url
        return context

    def form_valid(self, form):
        """Save changes to user group membership.

        Compares submitted groups with current assignments and applies
        additions and deletions using bulk operations.

        Args:
            form: Validated GroupsUserForm instance.

        Returns:
            HttpResponse: Redirect to success URL.
        """
        groups_objects = form.cleaned_data["auth_group"]
        new_groups_ids = set(grupo.id for grupo in groups_objects)

        current_ids = set(UserGroup.objects.filter(user=self.user).values_list("auth_group", flat=True))

        groups_ids_to_add = new_groups_ids - current_ids
        groups_ids_to_delete = current_ids - new_groups_ids

        new_objects = [grupo for grupo in groups_objects if grupo.id in groups_ids_to_add]
        bulk_create_with_history(
            [UserGroup(auth_group=grupo, user=self.user) for grupo in new_objects], model=UserGroup
        )

        if groups_ids_to_delete:
            UserGroup.objects.filter(user=self.user, auth_group__in=groups_ids_to_delete).delete()

        messages.success(self.request, self.success_message)
        return super().form_valid(form)
