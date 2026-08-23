"""Form definitions for albums, songs, and album merchandise."""

from datetime import timedelta

from crispy_forms.helper import FormHelper
from django import forms
from django.utils.text import format_lazy

from apps.comun.consts import (
    ERROR_MAX_VALUE,
    ERROR_MIN_LENGTH,
    ERROR_MIN_VALUE,
    ERROR_NEGATIVE_NUMBER,
    ERROR_REQUIRED_FIELD,
)
from apps.comun.forms import (
    AbstractModelForm,
    GenericBaseFormSet,
    GenericBaseInlineFormSet,
    MultipleTagField,
    SingleTagField,
)
from apps.music_genres.models import MusicGenres
from apps.music_tags.models import MusicTags
from apps.music_themes.models import MusicThemes
from apps.tipo_productos.models import TipoProducto

from . import consts
from .models import Album, AlbumGenreRelation, AlbumMerch, MerchProductTypeRelation, Song
from .widgets import MusicGenresTagWidget, MusicTagsSingleTagWidget, MusicThemesSingleTagWidget, TipoProductoTagWidget


class AlbumForm(AbstractModelForm):
    """Handles creation and update of album records.

    This form validates album uniqueness and manages related genre tags,
    including soft-delete aware synchronization.
    """

    primary_tag = SingleTagField(
        queryset=MusicTags.objects.all(),
        create_field="tag",
        widget=MusicTagsSingleTagWidget(),
        label=consts.ALBUM_PRIMARY_TAG_LABEL,
        required=False,
    )

    genres = MultipleTagField(
        queryset=MusicGenres.objects.all(),
        create_field="genre",
        widget=MusicGenresTagWidget(),
        label=consts.ALBUM_GENRES_LABEL,
    )

    def clean_title(self):
        """Validate that the title is present and not duplicated."""
        title = self.cleaned_data.get("title", "").strip()

        if not title:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)

        # Validate duplicates only on create or when the title changes on edit.
        if not self.instance.pk:
            # Create
            if Album.objects.filter(title=title, deleted__isnull=True).exists():
                raise forms.ValidationError(consts.ERROR_DUPLICATED_REGISTER)
        else:
            # Edit - validate only when the title changes.
            if self.instance.title != title:
                if Album.objects.filter(title=title, deleted__isnull=True).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError(consts.ERROR_DUPLICATED_REGISTER)

        return title

    def clean_artist(self):
        """Validate that the artist is present and not duplicated."""
        artist = self.cleaned_data.get("artist", "").strip()

        if not artist:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)

        # Validate duplicates only on create or when the artist changes on edit.
        if not self.instance.pk:
            # Create
            if Album.objects.filter(artist=artist, deleted__isnull=True).exists():
                raise forms.ValidationError(consts.ERROR_DUPLICATED_REGISTER)
        else:
            # Edit - validate only when the artist changes.
            if self.instance.artist != artist:
                if Album.objects.filter(artist=artist, deleted__isnull=True).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError(consts.ERROR_DUPLICATED_REGISTER)

        return artist

    def clean_year(self):
        """Validate that the year is greater than or equal to 1895."""
        year = self.cleaned_data["year"]
        if year < 1895:
            raise forms.ValidationError(format_lazy(ERROR_MIN_VALUE, min_value=1895))
        return year

    class Meta:
        model = Album
        fields = [
            "title",
            "year",
            "artist",
            "primary_tag",
            "genres",
            "cover",
        ]  # You can change this for the field"s name
        exclude = ["deleted", "created_by", "updated_by"]

        labels = {
            "title": consts.ALBUM_TITLE_LABEL,
            "year": consts.ALBUM_YEAR_LABEL,
            "artist": consts.ALBUM_ARTIST_LABEL,
            "cover": consts.ALBUM_COVER_LABEL,
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": consts.ALBUM_TITLE_PLACEHOLDER}),
            "year": forms.NumberInput(attrs={"placeholder": consts.ALBUM_YEAR_PLACEHOLDER}),
            "artist": forms.TextInput(attrs={"placeholder": consts.ALBUM_ARTIST_PLACEHOLDER}),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance: Album
        # If editing an existing album, filter out soft-deleted tags from initial display
        if self.instance and self.instance.pk:
            # Get only non-deleted tag relations
            active_relation_ids = AlbumGenreRelation.objects.filter(
                album=self.instance,
                deleted__isnull=True,
            ).values_list("genre_id", flat=True)
            active_genres = MusicGenres.objects.filter(id__in=active_relation_ids)
            self.fields["genres"].initial = active_genres
            self.fields["genres"].widget.value = active_genres
            self.initial["genres"] = active_genres

        if self.user:
            self.fields["primary_tag"].widget.user = self.user
            self.fields["genres"].widget.user = self.user

    def clean_primary_tag(self):
        """Validate that the primary tag is not assigned to another album.

        Soft-deleted records are ignored.
        """
        primary_tag = self.cleaned_data.get("primary_tag")
        if not primary_tag:
            return primary_tag

        qs = Album.objects.filter(primary_tag=primary_tag, deleted__isnull=True)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(consts.ERROR_DUPLICATED_PRIMARY_TAG)

        return primary_tag

    def clean_genres(self):
        """Validate that genres have allowed characters and are not too generic."""
        import re

        genres = self.cleaned_data.get("genres", [])

        # List of overly generic terms that are not allowed.
        generic_terms = ["music", "song", "audio", "sound", "track", "album"]

        # Regular expression for disallowed special characters.
        # Allow letters, numbers, spaces, hyphens, and apostrophes.
        special_chars_pattern = re.compile(r"[^a-zA-Z0-9\s\-\']")

        for genre in genres:
            genre_name = genre.genre if hasattr(genre, "genre") else str(genre)
            genre_name_lower = genre_name.lower().strip()

            # Validate special characters.
            if special_chars_pattern.search(genre_name):
                raise forms.ValidationError(format_lazy(consts.ERROR_GENRE_INVALID_CHARACTERS, genre_name=genre_name))

            # Validate that it is not too generic.
            if genre_name_lower in generic_terms:
                raise forms.ValidationError(format_lazy(consts.ERROR_GENRE_TOO_GENERIC, genre_name=genre_name))

        return genres

    def save(self, commit=True):
        """Saves the form instance, setting user fields if applicable.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            object: The saved model instance.
        """
        album = super().save(commit)
        genres = self.cleaned_data.get("genres", [])
        if commit:
            album.save()
            self._handle_genres(album, genres)
        else:
            # defer tags until save_m2m
            self._pending_genres = genres

        return album

    def _save_m2m(self):
        """Called by ModelForm when you saved with commit=False.

        Ensures tags are applied after album has a PK.
        """
        super()._save_m2m()
        if hasattr(self, "_pending_genres"):
            self._handle_genres(self.instance, self._pending_genres)
            del self._pending_genres

    def _handle_genres(self, album, tags):
        """Handle tag relations with proper soft delete support.

        This method will:
        1. Undelete existing soft-deleted relations if the tag is being re-added
        2. Soft delete relations for tags that are being removed
        3. Create new relations for truly new tags
        """
        # Get current tag IDs (including soft-deleted ones)
        current_relations = AlbumGenreRelation.objects.filter(album=album)
        current_genre_ids = set(current_relations.values_list("genre_id", flat=True))

        # Convert tags to IDs if they're model instances
        new_genre_ids = set()
        for tag in tags:
            if hasattr(tag, "pk"):
                new_genre_ids.add(tag.pk)
            else:
                new_genre_ids.add(int(tag))

        # Tags to be removed (soft delete)
        genres_to_remove = current_genre_ids - new_genre_ids
        if genres_to_remove:
            AlbumGenreRelation.objects.filter(
                album=album, genre_id__in=genres_to_remove
            ).delete()  # This will soft delete due to the policy

        # Tags to be added or undeleted
        for genre_id in new_genre_ids:
            try:
                # Try to get existing relation (including soft-deleted)
                relation = AlbumGenreRelation.all_objects.get(album=album, genre_id=genre_id)
                if relation.deleted is not None:
                    # Undelete the relation
                    relation.undelete()
            except AlbumGenreRelation.DoesNotExist:
                # Create new relation
                AlbumGenreRelation.objects.create(album=album, genre_id=genre_id)


class SongForm(AbstractModelForm):
    """Handles creation and update of songs linked to an album.

    This form validates title uniqueness, enforces minimum title length,
    and checks duration constraints.
    """

    duration = forms.DurationField(
        initial="00:00:00",
        label=consts.SONG_DURATION_LABEL,
        widget=forms.TimeInput(
            format="%H:%M:%S",
            attrs={
                "placeholder": consts.SONG_DURATION_PLACEHOLDER,
            },
        ),
    )

    theme = SingleTagField(
        queryset=MusicThemes.objects.all(),
        create_field="theme",
        widget=MusicThemesSingleTagWidget(),
        label=consts.SONG_THEME_LABEL,
        required=False,
    )

    class Meta:
        model = Song
        fields = ["title", "duration", "theme"]  # You can change this for the field"s name
        exclude = ["deleted", "created_by", "updated_by"]

        labels = {
            "title": consts.SONG_TITLE_LABEL,
            "duration": consts.SONG_DURATION_LABEL,
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": consts.SONG_TITLE_PLACEHOLDER}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields["title"].required = True

        if self.user:
            self.fields["theme"].widget.user = self.user

    def clean_title(self):
        """Validate the title field.

        Raises:
            forms.ValidationError: Whenever the field doesn't meet the requirements.

        Returns:
            str: The validated title.
        """
        title = self.cleaned_data["title"].strip()
        if len(title) < 2:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=2))

        # Validate that no other song has the same title globally.
        qs = Song.objects.filter(title__iexact=title, deleted__isnull=True)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(consts.ERROR_SONG_TITLE_EXISTS)

        return title

    def clean_duration(self):
        """Method to validate the duration field.

        Raises:
            forms.ValidationError: Whenever the field doesn't meet the requirements.

        Returns:
            timedelta: The validated duration.
        """
        duration: timedelta = self.cleaned_data["duration"]
        if duration.total_seconds() < 0:
            raise forms.ValidationError(ERROR_NEGATIVE_NUMBER)
        return duration


class SongInlineFormSet(GenericBaseInlineFormSet):
    """Validates inline song forms for minimum entries and duplicate titles."""

    def clean(self):  # noqa
        super().clean()
        songs_titles = []
        valid_forms = 0
        has_duplicates = False
        # Validate the formset for duplicates.
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                valid_forms += 1
                title = form.cleaned_data.get("title")
                if title in songs_titles:
                    form.add_error("title", consts.ERROR_DUPLICATED_SONG_TITLE)
                    has_duplicates = True
                songs_titles.append(title)

        if has_duplicates:
            raise forms.ValidationError(consts.ERROR_DUPLICATED_SONG_TITLE)

        if valid_forms < 1:
            raise forms.ValidationError(consts.ERROR_AT_LEAST_ONE_SONG)


class SongFormSet(GenericBaseFormSet):
    """Validates song formsets for duplicate titles and required rows."""

    def clean(self):  # noqa
        super().clean()
        songs_titles = []
        valid_forms = 0
        has_duplicates = False
        # Validate the formset for duplicates.
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                valid_forms += 1
                title = form.cleaned_data.get("title")
                if title in songs_titles:
                    form.add_error("title", consts.ERROR_DUPLICATED_SONG_TITLE)
                    has_duplicates = True
                songs_titles.append(title)

        if has_duplicates:
            raise forms.ValidationError(consts.ERROR_DUPLICATED_SONG_TITLE)

        if valid_forms < 1:
            raise forms.ValidationError(consts.ERROR_AT_LEAST_ONE_SONG)


class AlbumMerchForm(AbstractModelForm):
    """Handles creation and update of merchandise linked to an album.

    This form validates price and merchandise name and synchronizes related
    product type tags with soft-delete aware behavior.
    """

    product_types = MultipleTagField(
        queryset=TipoProducto.objects.all(),
        create_field="nombre",
        widget=TipoProductoTagWidget(),
        label=consts.MERCH_PRODUCT_TYPES_LABEL,
    )

    class Meta:
        model = AlbumMerch
        fields = ["merch_name", "price", "product_types"]  # You can change this for the field"s name
        exclude = ["deleted", "created_by", "updated_by"]

        labels = {
            "merch_name": consts.MERCH_NAME_LABEL,
            "price": consts.MERCH_PRICE_LABEL,
        }

        widgets = {
            "merch_name": forms.TextInput(attrs={"placeholder": consts.MERCH_NAME_PLACEHOLDER}),
            "price": forms.NumberInput(attrs={"placeholder": consts.MERCH_PRICE_PLACEHOLDER}),
        }

    def clean_price(self):
        """Validate that the price is non-negative and within a reasonable range."""
        price = self.cleaned_data.get("price")

        if price is None:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)

        if price < 0:
            raise forms.ValidationError(ERROR_NEGATIVE_NUMBER)

        if price > 999999.99:
            raise forms.ValidationError(format_lazy(ERROR_MAX_VALUE, max_value="999,999.99"))

        return price

    def clean_merch_name(self):
        """Validate that the merch name has at least 2 characters."""
        merch_name = self.cleaned_data.get("merch_name", "").strip()

        if not merch_name:
            raise forms.ValidationError(ERROR_REQUIRED_FIELD)

        if len(merch_name) < 2:
            raise forms.ValidationError(format_lazy(ERROR_MIN_LENGTH, min_length=2))

        return merch_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields["merch_name"].required = True
        self.fields["price"].required = True

        if self.instance and self.instance.pk:
            # Get only non-deleted tag relations.
            active_relation_ids = MerchProductTypeRelation.objects.filter(
                merch=self.instance,
                deleted__isnull=True,
            ).values_list("product_type_id", flat=True)
            active_product_types = TipoProducto.objects.filter(id__in=active_relation_ids)
            self.fields["product_types"].initial = active_product_types
            self.fields["product_types"].widget.value = active_product_types
            self.initial["product_types"] = active_product_types

        if self.user:
            self.fields["product_types"].widget.user = self.user

    def save(self, commit=True):  # noqa
        merch = super().save(commit)
        product_types = self.cleaned_data.get("product_types", [])
        if commit:
            merch.save()
            self._handle_product_types(merch, product_types)
        else:
            # Defer tags until save_m2m.
            self._pending_product_types = product_types

        return merch

    def _save_m2m(self):
        """Called by ModelForm when you saved with commit=False.

        Ensures tags are applied after album has a PK.
        """
        super()._save_m2m()
        if hasattr(self, "_pending_product_types"):
            self._handle_product_types(self.instance, self._pending_product_types)
            del self._pending_product_types

    def _handle_product_types(self, merch, tags):
        """Handle tag relations with proper soft delete support.

        This method will:
        1. Undelete existing soft-deleted relations if the tag is being re-added
        2. Soft delete relations for tags that are being removed
        3. Create new relations for truly new tags
        """
        # Get current tag IDs (including soft-deleted ones).
        current_relations = MerchProductTypeRelation.objects.filter(merch=merch)
        current_product_types_ids = set(current_relations.values_list("product_type_id", flat=True))

        # Convert tags to IDs if they're model instances.
        new_product_types_ids = set()
        for tag in tags:
            if hasattr(tag, "pk"):
                new_product_types_ids.add(tag.pk)
            else:
                new_product_types_ids.add(int(tag))

        # Tags to be removed (soft delete).
        product_types_to_remove = current_product_types_ids - new_product_types_ids
        if product_types_to_remove:
            MerchProductTypeRelation.objects.filter(
                merch=merch, product_type_id__in=product_types_to_remove
            ).delete()  # This will soft delete due to the policy

        # Tags to be added or undeleted.
        for product_type_id in new_product_types_ids:
            try:
                # Try to get existing relation (including soft-deleted)
                relation = MerchProductTypeRelation.all_objects.get(merch=merch, product_type_id=product_type_id)
                if relation.deleted is not None:
                    # Undelete the relation
                    relation.undelete()
            except MerchProductTypeRelation.DoesNotExist:
                # Create new relation
                MerchProductTypeRelation.objects.create(merch=merch, product_type_id=product_type_id)


class AlbumMerchInlineFormSet(GenericBaseInlineFormSet):
    """Validates inline merchandise forms for duplicate names."""

    def clean(self):  # noqa
        super().clean()
        merch_names = []
        valid_forms = 0
        # Validate the formset for duplicates.
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                valid_forms += 1
                merch_name = form.cleaned_data.get("merch_name")
                if merch_name in merch_names:
                    form.add_error("merch_name", consts.ERROR_DUPLICATED_MERCH_NAME)
                merch_names.append(merch_name)


class AlbumMerchFormSet(GenericBaseFormSet):
    """Validates merchandise formsets and business rules for product types."""

    def clean(self):  # noqa
        super().clean()
        merch_names = []
        valid_forms = 0
        # Validate the formset for duplicates.
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                valid_forms += 1
                merch_name = form.cleaned_data.get("merch_name")
                if merch_name in merch_names:
                    form.add_error("merch_name", consts.ERROR_DUPLICATED_MERCH_NAME)
                merch_names.append(merch_name)

                # Validate product_types.
                product_types = form.cleaned_data.get("product_types", [])

                # Validación 1: Verificar que los tipos de producto sean válidos
                for product_type in product_types:
                    if hasattr(product_type, "nombre"):
                        nombre = product_type.nombre
                    else:
                        # If it is a PK, load the object.
                        try:
                            product_type_obj = TipoProducto.objects.get(pk=product_type)
                            nombre = product_type_obj.nombre
                        except TipoProducto.DoesNotExist:
                            continue

                    # Validation: Minimum 3 characters.
                    if len(nombre) < 3:
                        form.add_error(
                            "product_types",
                            format_lazy(consts.ERROR_PRODUCT_TYPE_TOO_SHORT, name=nombre),
                        )

                    # Validation: Cannot start with special characters.
                    if nombre and not nombre[0].isalnum():
                        form.add_error(
                            "product_types",
                            format_lazy(consts.ERROR_PRODUCT_TYPE_INVALID_START, name=nombre),
                        )

                    # Validation: Cannot be only numbers.
                    if nombre.isdigit():
                        form.add_error(
                            "product_types",
                            format_lazy(consts.ERROR_PRODUCT_TYPE_ONLY_NUMBERS, name=nombre),
                        )

                    # Validation: Forbidden words.
                    forbidden_words = ["gratis", "test", "fake", "prueba", "demo", "spam"]
                    if nombre.lower() in forbidden_words:
                        form.add_error("product_types", format_lazy(consts.ERROR_PRODUCT_TYPE_FORBIDDEN, name=nombre))

                    # Validation: Maximum 5 words.
                    palabras = nombre.split()
                    if len(palabras) > 5:
                        form.add_error(
                            "product_types",
                            format_lazy(consts.ERROR_PRODUCT_TYPE_TOO_MANY_WORDS, name=nombre),
                        )

                    # Validation: Not too generic.
                    generic_words = ["cosa", "item", "producto", "objeto", "thing"]
                    if nombre.lower() in generic_words:
                        form.add_error(
                            "product_types",
                            format_lazy(consts.ERROR_PRODUCT_TYPE_TOO_GENERIC, name=nombre),
                        )
