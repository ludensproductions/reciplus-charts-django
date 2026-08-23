class AppError(Exception):
    """Structured application exception with error code, type and context."""

    def __init__(
        self,
        code: str,
        error_type: str,
        user_message: str,
        log_message: str | None = None,
        context: dict | None = None,
        status_code: int = 400,
    ) -> None:
        self.code = code
        self.type = error_type
        self.user_message = user_message
        self.log_message = log_message or user_message
        self.context = context or {}
        self.status_code = status_code
        super().__init__(self.log_message)
