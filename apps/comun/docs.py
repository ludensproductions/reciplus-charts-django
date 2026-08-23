import traceback
from typing import List, Type

from django.apps import apps
from django.views import View

from .consts import HistoriasUsuario


def get_views_by_hu(hu: HistoriasUsuario) -> List[Type[View]]:
    """
    Returns all views that implement a specific User Story (HU).

    Args:
        hu (HistoriasUsuario): The User Story to search for.
            Must follow the HU### format (e.g., HU001, HU002).
    """
    views_with_hu = []

    # Iterate over all installed apps
    for app_config in apps.get_app_configs():
        try:
            views_module = __import__(f"{app_config.name}.views", fromlist=[""])

            for attr_name in dir(views_module):
                attr = getattr(views_module, attr_name)

                if isinstance(attr, type) and issubclass(attr, View) and attr != View:
                    # Check if the class has Meta.HUs defined
                    if hasattr(attr, "Meta") and hasattr(attr.Meta, "HUs"):
                        if hu in attr.Meta.HUs:
                            views_with_hu.append(attr)

        except ImportError:
            traceback.print_exc()
            continue

    return views_with_hu


def get_hu_documentation() -> dict:
    """
    Generates documentation of the User Stories (HUs)
    and their relationship with system views.
    """
    documentation = {}

    for hu in HistoriasUsuario:
        views = get_views_by_hu(hu)

        documentation[hu.value] = {
            "views": [f"{view.__module__}.{view.__name__}" for view in views],
            "description": hu.describe(),
        }

    return documentation
