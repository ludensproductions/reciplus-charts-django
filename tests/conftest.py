import asyncio
import logging
import os
import re
import signal
import sys
from datetime import datetime
from pathlib import Path

# Add both tests directory and its parent to sys.path
# This allows both "from pages..." and "from tests.pages..." to work
tests_dir = Path(__file__).parent
sys.path.insert(0, str(tests_dir.parent))  # Enables "from tests.pages..."
sys.path.insert(0, str(tests_dir))  # Enables "from pages..."

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from playwright.async_api import Browser, BrowserContext, Playwright, async_playwright

from tests.pages.usuarios.page_login import LoginPage

load_dotenv()

# Configuración de logging
# Para activar logs de DEBUG, ejecuta pytest con: pytest --log-cli-level=DEBUG
# Para modo normal (sin logs de debug): pytest (por defecto solo mostrará WARNING y superiores)
logging.basicConfig(
    level=logging.WARNING,  # Nivel por defecto: solo WARNING y ERROR
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

record_screen = os.getenv("RECORD_SCREEN", "false").lower()
width = int(os.getenv("SCREEN_WIDTH", 1920))
height = int(os.getenv("SCREEN_HEIGHT", 1080))
headless = os.getenv("HEADLESS", "true").lower() == "true"

# Configurar event loop para Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


def handle_interrupt(signum, frame):
    """Manejador de señal SIGINT para Ctrl+C."""
    print("\nSalida forzada por Ctrl+C")
    os._exit(130)


signal.signal(signal.SIGINT, handle_interrupt)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Crea un event loop para la sesión de pruebas."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def playwright():
    """Inicia y provee la instancia de Playwright."""
    async with async_playwright() as p:
        yield p


@pytest_asyncio.fixture(scope="session")
async def browser(playwright: Playwright):
    """Inicia y provee la instancia del navegador Chromium."""
    browser = await playwright.chromium.launch(headless=True)
    yield browser
    await browser.close()


@pytest.fixture(scope="session", autouse=True)
def check_url_proyecto():
    """Verifica si la URL del proyecto contiene la palabra demo.

    Si la URL contiene demo, pregunta al usuario si desea continuar.
    """
    url_proyecto = os.getenv("URL_PROYECTO")
    if not url_proyecto:
        pytest.fail(
            "❌❌❌ ERROR CRÍTICO: La variable de entorno 'URL_PROYECTO' no está definida. ❌❌❌\n"
            "Por favor, define la variable de entorno antes de ejecutar las pruebas."
        )

    if "software-demo" in url_proyecto.lower():
        print(
            "❌❌❌ ERROR CRÍTICO: Estás corriendo las pruebas en el entorno de ejecución demo, cambia la URL para poder correr las pruebas. ❌❌❌\n"
            f"URL proporcionada: {url_proyecto}\n"
            "⚠️⚠️⚠️ ¡No se pueden ejecutar pruebas en un entorno de demo! ⚠️⚠️⚠️"
        )
        while True:
            answer = input("¿Deseas continuar con la ejecución de las pruebas? (si/no): ").strip().lower()
            if answer in ("si", "s"):
                return True
            elif answer in ("no", "n"):
                pytest.fail("¡No se pueden ejecutar pruebas en un entorno de demo!")
            else:
                print("Por favor, ingresa 'si' o 'no'.")


@pytest_asyncio.fixture(scope="function")
async def context(browser: Browser):
    """Browser context con configuración específica."""
    context = await browser.new_context(
        locale="es-ES",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        viewport={"width": width, "height": height},
        accept_downloads=True,
    )
    yield context
    await context.close()


@pytest_asyncio.fixture(scope="function")
async def page(context: BrowserContext, request):
    """Page con grabación de video opcional."""
    print("Iniciando prueba...", record_screen)

    if record_screen:
        # Directorios para guardar screenshots y videos
        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(base_dir, "media", "screenshots")
        videos_dir = os.path.join(base_dir, "media", "videos")

        # Crear carpetas si no existen
        os.makedirs(screenshot_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)

        # Formatear nombre y fecha
        match = re.search(r"\[([^\] ]+)", request.node.name)
        formated_name = match.group(1) if match else "test"
        formated_date = datetime.now().strftime("%d_%m_%y-%H_%M_%S")

        # Crear un nuevo contexto con grabación de video habilitada
        new_context = await context.browser.new_context(
            record_video_dir=videos_dir, record_video_size={"width": 1920, "height": 1080}
        )
        page = await new_context.new_page()

        yield page

        # Si la prueba falla, se toma un screenshot
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            try:
                screenshot_path = os.path.join(screenshot_dir, f"{formated_name}_{formated_date}.png")
                await page.screenshot(path=screenshot_path)
            except:
                pass

        await page.close()
        await new_context.close()

        # Manejar video
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            try:
                video_path = await page.video.path()
                new_video_path = os.path.join(videos_dir, f"{formated_name}_{formated_date}.webm")
                os.rename(video_path, new_video_path)
            except:
                pass
        else:
            try:
                await page.video.delete()
            except:
                pass

    else:
        page = await context.new_page()
        yield page
        await page.close()


# Necesario para que request.node.rep_call.failed funcione
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar el resultado de cada prueba."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_configure(config):
    """Configura la ruta del reporte HTML según el tipo de prueba."""
    test_files = [arg for arg in sys.argv[1:] if "test" in arg]

    subfolder = "e2e"
    for path in test_files:
        test_path = (Path.cwd() / path).resolve()
        if "unittest" in str(test_path):
            subfolder = "unittest"
            break

    base_dir = Path(__file__).parent
    report_dir = base_dir / subfolder

    report_dir.mkdir(exist_ok=True)

    if test_files:
        config.option.htmlpath = str(report_dir / "report" / "report.html")
    else:
        config.option.htmlpath = None


@pytest_asyncio.fixture
async def login_page(context):
    """Fixture to log in user."""

    async def _login_user(username, password):
        page = await context.new_page()

        if not username and not password:
            return page

        login_page = LoginPage(page, username, password)
        await login_page.login()
        return page

    return _login_user
