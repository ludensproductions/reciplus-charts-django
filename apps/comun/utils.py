import requests
from django.conf import settings

from .fields import PropertyField


# Helper function to create property-like objects
def create_field(view, name, model_fields, verbose_name=None):
    """Create a field-like object for either a model field or property.

    This helper function handles both regular model fields and properties,
    creating appropriate field objects that can be used in views.

    Args:
        view: The view instance that contains the model
        name (str): The name of the field or property
        model_fields (dict): Dictionary of the model's fields
        verbose_name (str, optional): A human-readable name for the field

    Returns:
        Field or PropertyField: The appropriate field object, or None if the field
            doesn't exist and isn't a property
    """
    if name in model_fields:
        field = model_fields[name]
        # Just modify the verbose_name without creating a new instance
        if verbose_name:
            field.verbose_name = verbose_name
        return field
    elif hasattr(view.model, name) and isinstance(getattr(view.model, name), property):
        return PropertyField(name, verbose_name)
    return None


def send_get_request(url, token, params=None):
    """Send a GET request to the specified URL with the given token and parameters.

    Args:
        url (str): The URL to send the request to.
        token (str): The authentication token to include in the request headers.
        params (dict, optional): The query parameters to include in the request.

    Returns:
        Response: The response object from the request.
    """
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, params=params)
    return response


def get_user_timezone(request):
    """Get the user's timezone from the request.

    Args:
        request: The HTTP request object.

    Returns:
        str: The user's timezone.
    """
    return request.session.get("django_timezone", settings.TIME_ZONE)
