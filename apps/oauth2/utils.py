import base64
import hashlib
import random
import string

from django.contrib.sessions.models import Session
from django.utils import timezone


def generate_code_verifier():
    verifier = "".join(random.choices(string.ascii_letters + string.digits, k=128))
    return base64.urlsafe_b64encode(verifier.encode("utf-8")).rstrip(b"=").decode("utf-8")


def generate_code_challenge(verifier):
    code_challenge = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode("utf-8")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def delete_all_unexpired_sessions_for_user(user):
    unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    [session.delete() for session in unexpired_sessions if str(user.pk) == session.get_decoded().get("_auth_user_id")]
