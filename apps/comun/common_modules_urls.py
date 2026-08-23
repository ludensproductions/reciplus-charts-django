from django.urls import path


def generate_crud_urls(views, lang="es", include=None):
    """Genera las URLs para un CRUD basándose en un diccionario de configuración.

    :param views: Objeto que contiene las vistas necesarias.
    :param lang: Idioma para las rutas ("es" o "en").
    :param include: Lista de nombres de URL a incluir (index, create, edit, delete, detail).
                    Si es None, se incluyen todas.
    :return: Lista de URL patterns de Django.
    """
    urls_config = {
        "index": {"es": "", "en": "", "view": "IndexView"},
        "create": {"es": "crear/", "en": "create/", "view": "CreateView"},
        "edit": {"es": "editar/<int:pk>", "en": "edit/<int:pk>", "view": "EditView"},
        "delete": {"es": "eliminar/<int:pk>", "en": "delete/<int:pk>", "view": "DeleteView"},
        "detail": {"es": "detalles/<int:pk>", "en": "detail/<int:pk>", "view": "DetailView"},
        "disabled_index": {"es": "deshabilitados/", "en": "disabled/", "view": "DisabledIndexView"},
    }

    if include is None:
        include = urls_config.keys()

    urlpatterns = []

    for key in include:
        config = urls_config.get(key)
        if config:
            view_class = getattr(views, config["view"], None)
            if view_class is None:
                continue
            route = config.get(lang, config["es"])
            urlpatterns.append(path(route, view_class.as_view(), name=key))

    return urlpatterns
