from django.utils.translation import gettext_lazy as _

APP_NAME = "catalogos"
CATALOGOS_TEMPLATE = "dashboard/catalogos.html"
CATALOGOS_URL = "catalogos:index"
CATALOGOS_TITLE = _("Catálogos")

# Model verbose names
MODEL_VERBOSE_NAME = _("Catálogo")
MODEL_VERBOSE_NAME_PLURAL = _("Catálogos")

# Permission labels
PERMISSION_VIEW_LABEL = _("Puede ver catálogos")


CATALOG_CARDS = [
    {
        "perm": None,
        "catalogo_url": "activity_feed:index",
        "title": _("Actividad"),
    },
    {"perm": "abarrotes.view_abarrotes", "catalogo_url": "abarrotes:index", "title": _("Abarrotes")},
    {"perm": "activities.view_activity", "catalogo_url": "activities:index", "title": _("Actividades")},
    {"perm": "albums.view_album", "catalogo_url": "albums:index", "title": _("Álbumes")},
    {"perm": "articles.view_article", "catalogo_url": "articles:index", "title": _("Artículos")},
    {"perm": "bodega.view_bodega", "catalogo_url": "bodega:index", "title": _("Bodega")},
    {"perm": "categories.view_category", "catalogo_url": "categories:index", "title": _("Categorías")},
    {
        "perm": None,
        "catalogo_url": "chat:index",
        "title": _("Chat"),
    },
    {"perm": "contents.view_content", "catalogo_url": "contents:index", "title": _("Contenidos")},
    {"perm": "students.view_student", "catalogo_url": "students:index", "title": _("Estudiantes")},
    {"perm": "music_tags.view_musictags", "catalogo_url": "music_tags:index", "title": _("Etiquetas musicales")},
    {"perm": "event_planner.view_event", "catalogo_url": "event_planner:index", "title": _("Eventos")},
    {"perm": "evidence.view_evidence", "catalogo_url": "evidence:index", "title": _("Evidencia")},
    {"perm": "facturas.view_factura", "catalogo_url": "facturas:index", "title": _("Facturas")},
    {"perm": "genres.view_genre", "catalogo_url": "genres:index", "title": _("Géneros")},
    {"perm": "music_genres.view_musicgenres", "catalogo_url": "music_genres:index", "title": _("Géneros musicales")},
    {
        "perm": "movie_inventory.view_movieinventory",
        "catalogo_url": "movie_inventory:index",
        "title": _("Inventario de películas"),
    },
    {
        "perm": "vehicle_brands.view_vehiclebrand",
        "catalogo_url": "vehicle_brands:index",
        "title": _("Marcas de vehículos"),
    },
    {"perm": "movies.view_movie", "catalogo_url": "movies:index", "title": _("Películas")},
    {"perm": "productos.view_producto", "catalogo_url": "productos:index", "title": _("Productos")},
    {
        "perm": "simple_report.view_simple_report",
        "catalogo_url": "simple_report:index",
        "title": _("Reportes simples"),
    },
    {
        "perm": "song_reviews.view_songreview",
        "catalogo_url": "song_reviews:index",
        "title": _("Reseñas de canciones"),
    },
    {"perm": "reservations.view_reservation", "catalogo_url": "reservations:index", "title": _("Reservaciones")},
    {"perm": "music_themes.view_musicthemes", "catalogo_url": "music_themes:index", "title": _("Temas musicales")},
    {
        "perm": "tipo_productos.view_tipoproducto",
        "catalogo_url": "tipo_productos:index",
        "title": _("Tipo productos"),
    },
    {
        "perm": "vehicle_types.view_vehicletype",
        "catalogo_url": "vehicle_types:index",
        "title": _("Tipos de vehículos"),
    },
    {"perm": "jobs.view_job", "catalogo_url": "jobs:index", "title": _("Trabajos")},
    {"perm": "sales.view_sale", "catalogo_url": "sales:index", "title": _("Ventas")},
    {"perm": "vehicles.view_vehicle", "catalogo_url": "vehicles:index", "title": _("Vehículos")},
    {"perm": "videos.view_video", "catalogo_url": "videos:index", "title": _("Videos")},
]
