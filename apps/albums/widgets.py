from apps.comun.select2.widgets import BaseModelSelect2TagWidget, ModelSelect2SingleTagWidget
from apps.music_genres.models import MusicGenres
from apps.music_tags.models import MusicTags
from apps.music_themes.models import MusicThemes
from apps.tipo_productos.models import TipoProducto


class TipoProductoTagWidget(BaseModelSelect2TagWidget):  # noqa
    model = TipoProducto
    search_fields = ["display_name__icontains"]

    def build_attrs(self, base_attrs, extra_attrs):
        """Add data-allow-clear to allow clearing the selected value."""
        extra_attrs = dict(extra_attrs or {})
        extra_attrs.setdefault("data-allow-clear", "true")
        return super().build_attrs(base_attrs, extra_attrs)


class MusicTagsSingleTagWidget(ModelSelect2SingleTagWidget):  # noqa
    model = MusicTags
    search_fields = ["tag__icontains"]


class MusicThemesSingleTagWidget(ModelSelect2SingleTagWidget):  # noqa
    model = MusicThemes
    search_fields = ["theme__icontains"]


class MusicGenresTagWidget(BaseModelSelect2TagWidget):  # noqa
    model = MusicGenres
    search_fields = ["genre__icontains"]

    def build_attrs(self, base_attrs, extra_attrs):
        """Add data-allow-clear to allow clearing the selected value."""
        extra_attrs = dict(extra_attrs or {})
        extra_attrs.setdefault("data-allow-clear", "true")
        return super().build_attrs(base_attrs, extra_attrs)
