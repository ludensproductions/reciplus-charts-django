import re

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django_q.tasks import async_task
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .consts import PASSWORD_RESET_EMAIL_SUBJECT, USER_WELCOME_EMAIL_SUBJECT


def is_anam_mail(email):
    """Return whether the email belongs to the ANAM domain."""
    if email is None:
        return False
    if re.fullmatch(r"^[a-zA-Z0-9_.]+@anam.gob.mx$", email, re.IGNORECASE):
        return True
    return False


def is_valid_mail(email):
    """Return whether the email matches the allowed format."""
    if email is None:
        return False
    if re.fullmatch(r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9-.]+$", email, re.IGNORECASE):
        return True
    return False


def send_password_reset_email(
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
):
    """Send password reset email with a centralized constant subject.

    Args:
        email_template_name (str): Plain text email template path.
        context (dict): Context used to render email templates.
        from_email (str): Sender email address.
        to_email (str): Recipient email address.
        html_email_template_name (str | None): Optional HTML template path.
    """
    subject = str(PASSWORD_RESET_EMAIL_SUBJECT)
    body = render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

    if html_email_template_name is not None:
        html_email = render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()


def generate_temporary_password(length=12):
    """Return a strong temporary password for newly created users."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%&*?"
    return get_random_string(length, alphabet)


def normalize_email(email):
    """Return a normalized email string suitable for matching."""
    if not email:
        return ""
    return email.strip().lower()


def get_deleted_username_candidate(username, next_deleted_count=None, max_length=None):
    """Return a soft-delete username suffix that preserves uniqueness within max length."""
    suffix_number = next_deleted_count or get_next_deleted_username_count(username)
    suffix = f"_delete_{suffix_number}"
    limit = max_length or get_username_max_length()
    base_username = username[: limit - len(suffix)]
    return f"{base_username}{suffix}"


def get_next_deleted_username_count(username):
    """Return the next numeric suffix for a deleted username variant."""
    from .models import User

    suffix_number = 1
    limit = get_username_max_length()

    while True:
        candidate = get_deleted_username_candidate(
            username,
            next_deleted_count=suffix_number,
            max_length=limit,
        )
        if not User.all_objects.filter(username=candidate).exists():
            return suffix_number
        suffix_number += 1


def get_username_max_length():
    """Return the configured max length for the username field."""
    from .models import User

    return User._meta.get_field("username").max_length


def get_available_username_input_max_length(username):
    """Return the maximum input length that still allows adding a delete suffix."""
    next_deleted_count = get_next_deleted_username_count(username)
    reserved_length = len(f"_delete_{next_deleted_count}")
    return max(1, get_username_max_length() - reserved_length)


def build_user_welcome_email_context(user, temporary_password):
    """Build the rendering context for the welcome credentials email."""
    protocol = "https" if getattr(settings, "SECURE_SSL_REDIRECT", False) else "http"
    domain = getattr(settings, "PASSWORD_RESET_BASE_URL", None) or getattr(settings, "DOMAIN", None) or "localhost:8000"
    domain = domain.replace("https://", "").replace("http://", "").strip("/")

    return {
        "user": user,
        "site_name": "Issirmax",
        "username": user.username,
        "temporary_password": temporary_password,
        "protocol": protocol,
        "domain": domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }


def send_user_welcome_email(user, temporary_password):
    """Queue the welcome credentials email using the project's current emailer pattern."""
    email_context = {
        "email": user.email,
        "subject": str(USER_WELCOME_EMAIL_SUBJECT),
        "body_template": "registration/user_welcome_email.html",
        "email_content": build_user_welcome_email_context(user, temporary_password),
    }
    async_task("apps.users.utils.send_credentials_email", email_context)


def send_credentials_email(context):
    """Send an HTML email using the shared async EmailMessage pattern."""
    email_message = EmailMessage(
        context["subject"],
        render_email_body(context["body_template"], context["email_content"]),
        to=[context["email"]],
    )
    email_message.content_subtype = "html"
    email_message.send()


def render_email_body(template_name, context):
    """Render an email template to HTML."""
    return render_to_string(template_name, context)
