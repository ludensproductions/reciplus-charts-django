import pytest
from pages.usuarios.page_perfil import PagePerfil

from utils.utils_functions import get_dotenv

env_config = get_dotenv()
user_admin = env_config.USER_ADMIN
password_admin = env_config.PASSWORD_ADMIN


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            user_admin,
            password_admin,
            id='PQA_HU006_001 Este caso de prueba tiene como propósito validar que el usuario "Administrador de sistema" pueda acceder al módulo "Perfil" para poder ver su información en el sistema.',
        ),
    ],
)
@pytest.mark.asyncio
async def test_view_profile(login_page, user, password):
    page = await login_page(user, password)
    perfil_page = PagePerfil(page)

    await perfil_page.validate_user_information(user)


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            user_admin,
            password_admin,
            id='PQA_HU006_002 Este caso de prueba tiene como propósito validar que el usuario "Administrador de sistema" pueda cambiar su imagen de perfil con un formato válido (jpg, jpeg, png y svg) en el módulo "Perfil".',
        )
    ],
)
@pytest.mark.asyncio
async def test_change_profile_picture(login_page, user, password):
    page = await login_page(user, password)
    perfil_page = PagePerfil(page)

    await perfil_page.change_profile_picture()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            user_admin,
            password_admin,
            id='PQA_HU006_003 Este caso de prueba tiene como propósito validar que el usuario "Administrador de sistema" no pueda cambiar su imagen de perfil con un formato no válido (doc, pdf, xlsx) en el módulo "Perfil".',
        )
    ],
)
@pytest.mark.asyncio
async def test_change_invalid_profile_picture(login_page, user, password):
    page = await login_page(user, password)
    perfil_page = PagePerfil(page)

    await perfil_page.change_invalid_profile_picture()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            user_admin,
            password_admin,
            id='PQA_HU006_004 Este caso de prueba tiene como propósito validar que el usuario "Administrador de sistema" pueda "Regresar" desde el módulo "Perfil".',
        )
    ],
)
@pytest.mark.asyncio
async def test_cancel_change_profile_picture(login_page, user, password):
    page = await login_page(user, password)
    perfil_page = PagePerfil(page)

    await perfil_page.cancel_change_profile_picture()


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(
            user_admin,
            password_admin,
            id='PQA_HU006_005 Este caso de prueba tiene como propósito validar que el usuario "Administrador de sistema" pueda remover su imagen de perfil en el módulo "Perfil".',
        )
    ],
)
@pytest.mark.asyncio
async def test_remove_profile_picture(login_page, user, password):
    page = await login_page(user, password)
    perfil_page = PagePerfil(page)

    await perfil_page.change_profile_picture()
    await perfil_page.remove_profile_picture()
