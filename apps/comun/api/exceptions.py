from pydantic_core import PydanticCustomError


class CustomValueError(PydanticCustomError):
    """Clase de error personalizado que evita el prefijo 'Value error' en validadores de Pydantic.

    Uso en field_validator de Pydantic:
        from apps.comun.api.exceptions import CustomValueError

        @field_validator("address")
        @classmethod
        def validate_address(cls, value, info):
            if not value:
                raise CustomValueError('Custom error message for address field')
            return value
    """

    def __new__(cls, message):  # noqa
        # Crear instancia de PydanticCustomError con tipo 'custom_error' y el mensaje
        instance = super().__new__(cls, "custom_error", message)
        return instance
