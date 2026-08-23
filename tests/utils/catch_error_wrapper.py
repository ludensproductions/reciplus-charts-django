import functools

import pytest


def catch_test_failures(func):
    """Decorador para capturar errores en métodos de PageObject.

    Permite agregar lógica adicional (logs, screenshots, etc.)
    cuando falle una prueba.
    """

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        if getattr(self, "_handling_failure", False):
            # Si ya estamos manejando un fallo, no repetir la lógica
            return await func(self, *args, **kwargs)

        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            if not getattr(self, "_handling_failure", False):
                self._handling_failure = True  # Marcamos que estamos en modo error
                try:
                    # Este print no se borra por que es feedback hacia el usuario cuando falle una prueba.
                    print("Borrando registro creado debido a error en la prueba...")
                    await self.delete_record()
                except Exception as cleanup_error:
                    # Este tampoco
                    print(f"Error al borrar registro: {cleanup_error}")
                finally:
                    self._handling_failure = False  # Resetear bandera
                    pytest.fail(str(e))

    return wrapper
