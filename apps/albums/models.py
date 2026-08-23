from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.albums import consts as albums_consts
from apps.comun.models import AbstractModel, AbstractNullableModel


class Album(AbstractModel):  # noqa
    """Store album details and related music metadata.

    This model represents an album with its title, year, artist, optional cover
    image, and relationships to songs, genres, and merchandise.

    Attributes:
        title (str): Album title.
        year (int): Release year.
        artist (str): Album artist.
        cover (Image | None): Optional cover image.
        primary_tag (MusicTags | None): Primary music tag.
        genres (QuerySet[MusicGenres]): Related genres.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    title = models.CharField(max_length=100, verbose_name=albums_consts.ALBUM_TITLE_LABEL)
    year = models.PositiveIntegerField(verbose_name=albums_consts.ALBUM_YEAR_LABEL)
    artist = models.CharField(max_length=100, verbose_name=albums_consts.ALBUM_ARTIST_LABEL)
    cover = models.ImageField(
        upload_to="album_covers/",
        null=True,
        blank=True,
        verbose_name=albums_consts.ALBUM_COVER_LABEL,
    )

    primary_tag = models.ForeignKey(
        "music_tags.MusicTags",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tag_primary_albums",
    )
    genres = models.ManyToManyField("music_genres.MusicGenres", through="AlbumGenreRelation", related_name="albums")

    # Relations deleted when the album is deleted.
    delete_on_cascade = ["songs"]

    class Meta:
        db_table = "albums"
        verbose_name = albums_consts.ALBUM_VERBOSE_NAME
        verbose_name_plural = albums_consts.ALBUM_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):  # noqa
        """Return the album title for display.

        Returns:
            str: Album title.
        """
        return albums_consts.ALBUM_DISPLAY.format(album=self.title)


class Song(AbstractModel):  # noqa
    """Store a song belonging to an album."""

    _safedelete_policy = SOFT_DELETE_CASCADE
    title = models.CharField(max_length=100, verbose_name=albums_consts.SONG_TITLE_LABEL)
    duration = models.DurationField(verbose_name=albums_consts.SONG_DURATION_LABEL)
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="songs",
        verbose_name=albums_consts.SONG_ALBUM_LABEL,
    )

    theme = models.ForeignKey(
        "music_themes.MusicThemes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="theme_songs",
    )
    parent_relations = [(albums_consts.ALBUM_VERBOSE_NAME_PLURAL, "album", "albums:index")]

    class Meta:
        db_table = "songs"
        verbose_name = albums_consts.SONG_VERBOSE_NAME
        verbose_name_plural = albums_consts.SONG_VERBOSE_NAME_PLURAL
        ordering = ["created_at", "id"]

    def __str__(self):  # noqa
        """Return a display string for the song.

        Returns:
            str: Album and song title.
        """
        return albums_consts.SONG_DISPLAY.format(album=self.album.title, title=self.title)


class AlbumMerch(AbstractModel):  # noqa
    """Store merchandise items associated with an album."""

    _safedelete_policy = SOFT_DELETE_CASCADE
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="merch",
        verbose_name=albums_consts.MERCH_ALBUM_LABEL,
    )
    merch_name = models.CharField(max_length=100, verbose_name=albums_consts.MERCH_NAME_LABEL)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=albums_consts.MERCH_PRICE_LABEL)

    product_types = models.ManyToManyField(
        "tipo_productos.TipoProducto", through="MerchProductTypeRelation", related_name="merchs"
    )
    parent_relations = [(albums_consts.ALBUM_VERBOSE_NAME_PLURAL, "album", "albums:index")]

    class Meta:
        db_table = "album_merch"
        verbose_name = albums_consts.ALBUM_MERCH_VERBOSE_NAME
        verbose_name_plural = albums_consts.ALBUM_MERCH_VERBOSE_NAME_PLURAL
        ordering = ["created_at", "id"]

    def __str__(self):  # noqa
        """Return a display string for album merch.

        Returns:
            str: Album and merch name.
        """
        return albums_consts.MERCH_DISPLAY.format(album=self.album, merch=self.merch_name)


class AlbumGenreRelation(AbstractNullableModel):  # noqa
    """Relate albums to genres."""

    _safedelete_policy = SOFT_DELETE_CASCADE
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="album_genres",
        verbose_name=albums_consts.ALBUM_VERBOSE_NAME,
    )
    genre = models.ForeignKey(
        "music_genres.MusicGenres",
        on_delete=models.CASCADE,
        related_name="genre_albums",
        verbose_name=albums_consts.ALBUM_GENRE_LABEL,
    )

    class Meta:
        db_table = "album_genre_relations"
        verbose_name = albums_consts.ALBUM_GENRE_RELATION_VERBOSE_NAME
        verbose_name_plural = albums_consts.ALBUM_GENRE_RELATION_VERBOSE_NAME_PLURAL
        unique_together = ("album", "genre")
        ordering = ["created_at"]

    def __str__(self):  # noqa
        """Return a display string for the album-genre relation.

        Returns:
            str: Album and genre summary.
        """
        return albums_consts.ALBUM_GENRE_DISPLAY.format(album=self.album.title, genre=self.genre.genre)


class MerchProductTypeRelation(AbstractNullableModel):  # noqa
    """Relate album merch items to product types."""

    _safedelete_policy = SOFT_DELETE_CASCADE
    merch = models.ForeignKey(
        AlbumMerch,
        on_delete=models.CASCADE,
        related_name="merch_types",
        verbose_name=albums_consts.ALBUM_MERCH_VERBOSE_NAME,
    )
    product_type = models.ForeignKey(
        "tipo_productos.TipoProducto",
        on_delete=models.CASCADE,
        related_name="type_merchs",
        verbose_name=albums_consts.MERCH_PRODUCT_TYPES_LABEL,
    )

    class Meta:
        db_table = "merch_product_type_relations"
        verbose_name = albums_consts.MERCH_PRODUCT_TYPE_RELATION_VERBOSE_NAME
        verbose_name_plural = albums_consts.MERCH_PRODUCT_TYPE_RELATION_VERBOSE_NAME_PLURAL
        unique_together = ("merch", "product_type")
        ordering = ["created_at"]

    def __str__(self):  # noqa
        """Return a display string for the merch-product type relation.

        Returns:
            str: Merch and product type summary.
        """
        return albums_consts.MERCH_PRODUCT_TYPE_DISPLAY.format(
            merch=self.merch.merch_name,
            product_type=self.product_type.display_name,
        )
