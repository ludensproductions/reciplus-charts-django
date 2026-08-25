"""Vista de la página de gráficas."""
from django.conf import settings
from django.contrib.auth import login as django_login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from apps.graphs.auth import has_graphs_access
from apps.graphs.auth_bridge import redeem_exchange_code


def index(request):
    # Nativo (Android/iOS/Desktop): trae ?code=<codigo de un solo uso>, se canjea
    # aquí y se establece sesión Django real — de ahí en adelante igual que web.
    code = request.GET.get("code")
    if code and not has_graphs_access(request.user):
        user = redeem_exchange_code(code)
        if user is not None:
            django_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("graphs:index")  # limpia el código de la URL/historial

    if not has_graphs_access(request.user):
        return HttpResponseForbidden("No has iniciado sesión. Entra desde la app Reciplus.")

    return render(request, "graphs/index.html", {"frontend_url": settings.FRONTEND_URL})
