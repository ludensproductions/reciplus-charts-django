from ninja import Schema


class LogoutUser(Schema):
    """Schema for the centralized logout payload from the OAuth2 provider."""

    user_id: str


class LogoutResponseOut(Schema):
    """Schema for the logout endpoint response."""

    message: str
