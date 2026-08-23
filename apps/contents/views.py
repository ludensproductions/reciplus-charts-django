from typing import Type, Union

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import format_lazy

from apps.articles.forms import ArticleForm
from apps.comun.consts import ERROR_DISABLE_ALREADY_DISABLED
from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.contents.consts import ContentTypes
from apps.contents.forms import ContentForm
from apps.contents.models import Content
from apps.videos.forms import VideoForm

from .consts import (
    CREATE_TITLE,
    CREATE_URL,
    CUSTOM_JS_FILES,
    DASHBOARD_URL,
    DEFAULT_ORDERING,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    FILTER_FIELDS,
    FORM_TEMPLATE,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    MODEL_VERBOSE_NAME,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter content entries."""

    permission_required = PERMISSION_VIEW
    model = Content
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    verbose_name = MODEL_VERBOSE_NAME
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    edit_url = EDIT_URL
    detail_url = DETAIL_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create new content with the selected subtype."""

    permission_required = PERMISSION_ADD
    model = Content
    template_name: str = FORM_TEMPLATE
    form_class = ContentForm
    article_form_class = ArticleForm
    video_form_class = VideoForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL
    custom_js_files = CUSTOM_JS_FILES

    def create_form_instance(
        self,
        form_class: Union[Type[ArticleForm], Type[VideoForm]],
        request=None,
    ):
        """Create an instance of the specified form.

        Args:
            form_class (type): Article or video form class.
            request (HttpRequest | None): Optional request for POST data.

        Returns:
            forms.Form: Instantiated form with the appropriate prefix.
        """
        prefix = "article" if form_class == ArticleForm else "video"
        return form_class(request.POST if request else None, prefix=prefix)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """Handle POST requests to create content and its subtype.

        Returns:
            HttpResponse: Redirect on success or a rendered response with errors.
        """
        # Generic detail/edit context helpers expect self.object to exist.
        # In create flows this must be None until a valid object is saved.
        self.object = None
        content_form = self.form_class(request.POST)
        article_form = self.create_form_instance(ArticleForm, request)
        video_form = self.create_form_instance(VideoForm, request)

        if content_form.is_valid():
            self.object = content_form.save(commit=False)
            self.object.save()
            ctype = self.object.content_type

            # Validate dependent form
            if ctype == ContentTypes.ARTICLE.value and article_form.is_valid():
                article = article_form.save(commit=False)
                article.content = self.object
                article.save()

                if self.get_success_message(cleaned_data=content_form.cleaned_data):
                    messages.success(self.request, self.get_success_message(content_form.cleaned_data))

                return redirect(self.get_success_url())

            elif ctype == ContentTypes.VIDEO.value and video_form.is_valid():
                video = video_form.save(commit=False)
                video.content = self.object
                video.save()

                if self.get_success_message(cleaned_data=content_form.cleaned_data):
                    messages.success(self.request, self.get_success_message(content_form.cleaned_data))

                return redirect(self.get_success_url())

        # Re-render with errors when invalid.
        # Only bind POST data to the sub-form that matches the selected content_type.
        # The inactive sub-form is instantiated unbound because Django evaluates
        # form.errors when the template renders it, which would expose spurious
        # validation errors (e.g. the JS sends "" for hidden fields, triggering a
        # "field required" error on the inactive form alongside the real user error).
        selected_type = request.POST.get("content_type")
        context = self.get_context_data()
        context["form"] = content_form
        context["article_form"] = (
            article_form if selected_type == ContentTypes.ARTICLE.value else self.create_form_instance(ArticleForm)
        )
        context["video_form"] = (
            video_form if selected_type == ContentTypes.VIDEO.value else self.create_form_instance(VideoForm)
        )
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """Build the context with article and video forms.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)
        context["article_form"] = self.create_form_instance(ArticleForm)
        context["video_form"] = self.create_form_instance(VideoForm)
        return context


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Edit existing content entries and their subtypes."""

    permission_required = PERMISSION_CHANGE
    model = Content
    template_name: str = FORM_TEMPLATE
    form_class = ContentForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL
    custom_js_files = CUSTOM_JS_FILES

    def create_form_instance(
        self,
        form_class: Union[Type[ArticleForm], Type[VideoForm]],
        request=None,
        instance=None,
    ):
        """Create an instance of the specified form.

        Args:
            form_class (type): Article or video form class.
            request (HttpRequest | None): Optional request for POST data.
            instance (Model | None): Existing instance for edit mode.

        Returns:
            forms.Form: Instantiated form with the appropriate prefix.
        """
        prefix = "article" if form_class == ArticleForm else "video"
        return form_class(request.POST if request else None, prefix=prefix, instance=instance)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """Handle POST requests to update content and its subtype.

        Returns:
            HttpResponse: Redirect on success or a rendered response with errors.
        """
        self.object = self.get_object()
        content_form = self.form_class(request.POST, instance=self.object)
        content_type = request.POST.get("content_type")

        if self.object and hasattr(self.object, "article"):
            article_form = self.create_form_instance(ArticleForm, request=request, instance=self.object.article)
        else:
            article_form = self.create_form_instance(ArticleForm, request=request)

        if self.object and hasattr(self.object, "video"):
            video_form = self.create_form_instance(VideoForm, request=request, instance=self.object.video)
        else:
            video_form = self.create_form_instance(VideoForm, request=request)

        # Validate the main form.
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.save()

            # Handle dependent form based on content_type.
            if content_type == ContentTypes.ARTICLE.value:
                if article_form.is_valid():
                    article = article_form.save(commit=False)
                    article.content = content
                    article.save()
                    if article.deleted:
                        article.undelete()
                    content.article = article
                    if hasattr(content, "video"):
                        content.video.delete()
                    if self.get_success_message(cleaned_data=content_form.cleaned_data):
                        messages.success(self.request, self.get_success_message(content_form.cleaned_data))
                    return redirect(self.success_url)

            elif content_type == ContentTypes.VIDEO.value:
                if video_form.is_valid():
                    video = video_form.save(commit=False)
                    video.content = content
                    video.save()
                    if video.deleted:
                        video.undelete()
                    content.video = video
                    if hasattr(content, "article"):
                        content.article.delete()
                    if self.get_success_message(cleaned_data=content_form.cleaned_data):
                        messages.success(self.request, self.get_success_message(content_form.cleaned_data))
                    return redirect(self.success_url)

        # Re-render with errors when invalid.
        # Only bind POST data to the sub-form that matches the selected content_type.
        # The inactive sub-form is instantiated unbound because Django evaluates
        # form.errors when the template renders it, which would expose spurious
        # validation errors (e.g. the JS sends "" for hidden fields, triggering a
        # "field required" error on the inactive form alongside the real user error).
        context = self.get_context_data()
        context["form"] = content_form
        if content_type == ContentTypes.ARTICLE.value:
            context["article_form"] = article_form
            context["video_form"] = self.create_form_instance(VideoForm)
        elif content_type == ContentTypes.VIDEO.value:
            context["article_form"] = self.create_form_instance(ArticleForm)
            context["video_form"] = video_form
        else:
            # No valid content_type selected: both sub-forms are unbound so neither
            # shows field-level errors that would distract from the main form error.
            context["article_form"] = self.create_form_instance(ArticleForm)
            context["video_form"] = self.create_form_instance(VideoForm)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """Build the context with article and video forms.

        Returns:
            dict[str, Any]: Template context.
        """
        context = super().get_context_data(**kwargs)

        if self.object and hasattr(self.object, "article"):
            context["article_form"] = self.create_form_instance(ArticleForm, instance=self.object.article)
        else:
            context["article_form"] = self.create_form_instance(ArticleForm)

        if self.object and hasattr(self.object, "video"):
            context["video_form"] = self.create_form_instance(VideoForm, instance=self.object.video)
        else:
            context["video_form"] = self.create_form_instance(VideoForm)

        return context


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete or disable content entries."""

    permission_required = PERMISSION_DELETE
    model = Content
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True

    def post(self, request, *args, **kwargs):
        """Handle delete or disable requests.

        Returns:
            HttpResponse: Response from the delete handler.
        """
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
        self.object.undelete_specific_content()

        return self.handle_response(deleted, message)

    def delete(self, request, *args, **kwargs):
        """Delete the object and its associated subtype.

        Returns:
            HttpResponse: Response from the delete handler.
        """
        self.object = self.get_object()
        deleted, message = self.object.delete()

        self.object.delete_specific_content()

        return self.handle_response(deleted, message)


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Display details for a content entry."""

    permission_required = PERMISSION_VIEW
    model = Content
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    title = DETAIL_TITLE
    view_deleted_objects = True
