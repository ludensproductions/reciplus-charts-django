# 🧪 Framework de Testing Automatizado - Django Template

## 📋 Tabla de Contenidos

- [🎯 Descripción General](#descripción-general)
- [🏗️ Arquitectura del Framework](#arquitectura-del-framework)
- [🔧 Configuración e Instalación](#configuración-e-instalación)
- [📖 Archivos Base del Framework](#archivos-base-del-framework)
- [� Ejemplos Prácticos Reales](#ejemplos-prácticos-reales)
- [� Métodos Principales de GenericPage](#métodos-principales-de-genericpage)
- [🛠️ Utilidades y Herramientas](#utilidades-y-herramientas)
- [🎥 Grabación y Screenshots](#grabación-y-screenshots)
- [🚀 Mejores Prácticas](#mejores-prácticas)
- [🔍 Troubleshooting y FAQ](#troubleshooting-y-faq)

## 🎯 Descripción General

Este framework de testing automatizado está diseñado específicamente para aplicaciones Django, utilizando **Playwright** como motor de automatización web. Proporciona una arquitectura robusta basada en el patrón **Page Object Model** con generación automática de datos y manejo inteligente de dependencias.

### ✨ Características Principales

- 🎭 **Playwright Integration**: Motor de automatización web moderno y confiable
- 🏗️ **Page Object Model**: Código organizado y mantenible
- 🔄 **Generación Automática de Datos**: Basada en tipos de campo y Factory Pattern
- 📦 **Manejo de Dependencias**: Sistema automático para relaciones entre entidades
- 📋 **Formsets Dinámicos**: Soporte completo para formularios complejos
- 🎬 **Grabación de Videos**: Evidencia automática en caso de fallos
- 🧪 **Validaciones Comprehensivas**: Tests de datos válidos e inválidos

## 🏗️ Arquitectura del Framework

### 📁 Estructura de Directorios

```
tests/
├── 📂 pages/
│   ├── 📂 base_pages/          # Clases base del framework
│   │   ├── 📄 base_page.py     # Funcionalidades core de Playwright
│   │   ├── 📄 constants.py     # Enums y mensajes de error
│   │   ├── 📄 fields_page.py   # Manejo individual de campos
│   │   ├── 📄 generic_page.py  # Operaciones CRUD genéricas
│   │   └── 📄 standard_django_page.py # Extensiones para Django
│   ├── 📂 catalogos/           # Page Objects específicos
│   └── 📄 login_page.py        # Autenticación
├── 📂 e2e/                     # Tests end-to-end
│   ├── 📂 catalogos/           # Tests por módulo
│   └── 📂 usuarios/            # Tests de usuarios
├── 📂 utils/                   # Utilidades
│   ├── 📂 input_values_generation/ # Generadores de datos
│   └── 📄 utils_functions.py   # Funciones auxiliares
├── 📂 media/                   # Evidencias
│   ├── 📂 screenshots/         # Capturas de pantalla
│   └── 📂 videos/             # Grabaciones de video
├── 📄 conftest.py             # Configuración de pytest
└── 📄 README.md               # Esta documentación
```

### 🎯 Flujo de Herencia

```
BasePage
└── StandardDjangoPage
    └── GenericPage
        └── PageObjects Específicos (ej: PageEventos)

FieldsPage (para campos individuales)
Constants (enums y constantes)
```

## 🔧 Configuración e Instalación

### 📋 Instalación

```bash
# Para Unix (MacOS/Linux)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install

# Para Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
```

### ⚙️ Variables de Entorno

Crear archivo `.env` en el directorio `tests/`:

```env
# Configuración básica
URL_PROYECTO=http://localhost:8000
USER_ADMIN=admin
PASSWORD_ADMIN=12345

# Grabación (opcional)
RECORD_SCREEN=false
```

### 🎯 Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar archivo específico
pytest tests/e2e/catalogos/test_eventos.py

# Ejecutar con ID específico
pytest -k "EVT_01"

# Ejecutar con output detallado
pytest -s -v

# Ejecutar test específico
pytest -k "test_complete_crud_operations"
```

### 📝 Sistema de Logging

El framework implementa un sistema de logging que reemplaza los `print` statements por loggers de tipo `DEBUG`. Esto permite controlar cuándo ver información de depuración.

#### Modos de Ejecución:

```bash
# Modo normal (sin logs de debug)
pytest
# Solo muestra WARNING y ERROR

# Modo debug (muestra todos los logs)
pytest --log-cli-level=DEBUG
# Muestra información detallada de validaciones, dependencias, etc.

# Debug solo para módulos específicos
pytest --log-cli-level=DEBUG --log-file=test_debug.log
# Guarda logs en archivo

# Combinado con otras opciones
pytest -s -v --log-cli-level=DEBUG -k "CREAR_005"
```

#### Niveles de Log:
- **DEBUG**: Información detallada para debugging (dependencias, validaciones, valores de campos)
- **INFO**: Información general del flujo
- **WARNING**: Advertencias (valor de filtro incorrecto, campos faltantes)
- **ERROR**: Errores durante la ejecución

#### Personalización:

Para cambiar el nivel de logging por defecto, edita `tests/conftest.py`:

```python
logging.basicConfig(
    level=logging.WARNING,  # Cambia a DEBUG, INFO, etc.
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 📖 Archivos Base del Framework

### 🎭 BasePage (`base_page.py`)

Clase base que proporciona funcionalidades core de Playwright:

#### 🔑 Características Principales

- **Decorador automático de errores**: Aplica `catch_test_failures` a todos los métodos async
- **Interacción inteligente con formularios**: `fill_data()` detecta tipos de campo automáticamente
- **Validaciones comprehensivas**: Métodos para validar en vistas índice, detalle y edición
- **Manipulación de atributos HTML**: Remover `required`, `disabled`, etc.

#### �️ Métodos Principales

| Método                                               | Descripción                                         |
| ----------------------------------------------------- | ---------------------------------------------------- |
| `fill_data(data)`                                   | Rellena formulario automáticamente detectando tipos |
| `validate_edit_view_item_information(data)`         | Valida datos en formulario de edición               |
| `validate_record_information_in_details_view(data)` | Valida datos en vista de detalle                     |
| `validate_record_information_in_index_view(data)`   | Valida datos en tabla índice                        |
| `search_records_with_filters(filters)`              | Aplica filtros y busca                               |
| `wait_for_selector(selector)`                       | Espera elemento visible                              |

### 📊 Constants (`constants.py`)

Centraliza constantes, mensajes de error y enumeraciones:

#### �️ Enumeraciones Principales

```python
class ValidDataType(Enum):
    LETTERS = auto()           # Solo letras
    NUMBERS = auto()           # Solo números
    ALPHANUMERIC = auto()      # Letras y números
    EMAIL = auto()             # Email válido
    SPECIAL_CHARS = auto()     # Caracteres especiales
    ALLOW_DUPLICATES = auto()  # Permite duplicados

class InvalidDataType(Enum):
    REQUIRED = auto()          # Campo requerido vacío
    MAX_LENGTH = auto()        # Excede longitud máxima
    MIN_LENGTH = auto()        # No alcanza longitud mínima
    MIN_VALUE = auto()         # Valor menor al mínimo

class InputType(Enum):
    TEXT = auto()              # Campo de texto
    NUMBER = auto()            # Campo numérico
    DATE = auto()              # Campo de fecha
    SELECT = auto()            # Select estándar
    SELECT2 = auto()           # Select2 con búsqueda
    SELECT2_MULTIPLE = auto()  # Select2 múltiple
    # ... más tipos
```

### 🔧 FieldsPage (`fields_page.py`)

Representa campos individuales con validaciones específicas:

#### 🏗️ Constructor Real

```python
FieldsPage(
    page=page,
    field_selector='input[name="titulo"]',  # Selector CSS
    name="titulo",                          # Nombre del campo
    max_length=200,                         # Validaciones
    required=True,
    input_type=InputType.TEXT,
    is_generated_field=False,               # Si se genera automáticamente
    title_for_validate="get_title_name"     # Es el titulo definido en los detalles
)
```

### 🎭 GenericPage (`generic_page.py`)

Clase base para operaciones CRUD con atributos como diccionarios:

#### 🏗️ Estructura Real

```python
class PageEventos(GenericPage):
    def __init__(self, page):
        super().__init__(page, "Eventos", ["Catálogos", "Eventos"])

        # Campos se configuran como atributo de clase (diccionario)
        self.input_field_instances = {
            "titulo": FieldsPage(...),
            "ubicacion": FieldsPage(...),
            "responsable": FieldsPage(...),
        }

        # Dependencias entre páginas
        self.input_field_dependencies = {
            PageUsuarios: {
                DependencyAction.CREATE: {
                    "responsable": ["nombres", " ", "apellido_paterno"]
                },
            }
        }

        # Formsets
        self.formset_fields = {
            "activities": {
                "required": True,
                "fields": {
                    "activity": FieldsPage(...),
                    "capacity": FieldsPage(...),
                }
            }
        }
```

## � Ejemplos Prácticos Reales

### 🎬 Page Object Real: Eventos

```python
from enum import Enum
from pages.base_pages.fields_page import FieldsPage, InputType
from pages.base_pages.generic_page import GenericPage

class FieldEventoEnum(Enum):
    """Enum para evitar hardcodear strings."""
    TITULO = "title"
    FECHA_INICIO = "date_start"
    UBICACION = "location"
    RESPONSABLE = "responsible"
    FOLIO = "folio"  # Campo generado

class PageEventos(GenericPage):
    def __init__(self, page):
        super().__init__(page, "Eventos", ["Catálogos", "Eventos"])

        self.input_field_instances = {
            FieldEventoEnum.TITULO.value: FieldsPage(
                page=page,
                max_length=200,
                name=FieldEventoEnum.TITULO.value,
                field_selector=f'input[name="{FieldEventoEnum.TITULO.value}"]',
            ),
            FieldEventoEnum.UBICACION.value: FieldsPage(
                page=page,
                max_length=200,
                name=FieldEventoEnum.UBICACION.value,
                field_selector=f'input[name="{FieldEventoEnum.UBICACION.value}"]',
            ),
            FieldEventoEnum.RESPONSABLE.value: FieldsPage(
                page=page,
                name=FieldEventoEnum.RESPONSABLE.value,
                field_selector=f"#div_id_{FieldEventoEnum.RESPONSABLE.value}",
                input_type=InputType.SELECT2,
            ),
            # Campo generado automáticamente
            FieldEventoEnum.FOLIO.value: FieldsPage(
                page=page,
                name=FieldEventoEnum.FOLIO.value,
                field_selector=f'th[name="{FieldEventoEnum.FOLIO.value}"]',
                is_generated_field=True,  # No se llena en formularios
            ),
        }
```

### 🧪 Tests Reales del Framework

```python
import pytest
from pages.catalogos.page_evento import FieldEventoEnum, PageEventos
from pages.base_pages.fields_page import InvalidDataType, ValidDataType
from utils.user_const import USER_ADMIN, PASSWORD_ADMIN

# Test CRUD completo
@pytest.mark.parametrize("user, password", [
    pytest.param(USER_ADMIN, PASSWORD_ADMIN, id="EVT_01 CRUD completo evento"),
])
@pytest.mark.asyncio
async def test_complete_crud_operations(login_page, user, password):
    """Test completo de operaciones CRUD."""
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record()      # Crea con datos aleatorios
    await eventos.validate_record()    # Valida en detalle o edición
    await eventos.edit_record()        # Edita con nuevos datos
    await eventos.validate_record()    # Valida cambios
    await eventos.delete_record()      # Elimina y limpia dependencias

# Test solo campos requeridos
@pytest.mark.asyncio
async def test_create_only_required_fields(login_page, user, password):
    page = await login_page(user, password)
    eventos = PageEventos(page)

    await eventos.create_record(only_required=True)
    await eventos.validate_record()
    await eventos.delete_record()

# Tests de validaciones con datos inválidos
@pytest.mark.parametrize("user, password, field, validate_type, error_message", [
    pytest.param(
        USER_ADMIN, PASSWORD_ADMIN,
        FieldEventoEnum.TITULO.value,
        InvalidDataType.REQUIRED,
        None,
        id="EVT_03 No crear evento sin título",
    ),
    pytest.param(
        USER_ADMIN, PASSWORD_ADMIN,
        FieldEventoEnum.UBICACION.value,
        InvalidDataType.REQUIRED,
        "La ubicación es obligatoria.",
        id="EVT_04 No crear evento sin ubicación",
    ),
])
@pytest.mark.asyncio
async def test_required_fields_validation(login_page, user, password, field, validate_type, error_message):
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Método real del framework para validaciones inválidas
    await eventos.validate_create_invalid_data(field, validate_type, error_message)

# Tests con datos válidos
@pytest.mark.parametrize("user, password, field, validate_data_type", [
    pytest.param(
        USER_ADMIN, PASSWORD_ADMIN,
        FieldEventoEnum.TITULO.value,
        ValidDataType.SPECIAL_CHARS,
        id="EVT_15 Crear evento con título con caracteres especiales",
    ),
])
@pytest.mark.asyncio
async def test_valid_data_creation(login_page, user, password, field, validate_data_type):
    page = await login_page(user, password)
    eventos = PageEventos(page)

    # Método real del framework para validaciones válidas
    await eventos.validate_create_valid_data(field, validate_data_type)
```

## � Métodos Principales de GenericPage

### 🔄 Operaciones CRUD

| Método               | Descripción                       | Parámetros Principales                            |
| --------------------- | ---------------------------------- | -------------------------------------------------- |
| `create_record()`   | Crea registro con datos aleatorios | `only_required=False`, `validate_record=False` |
| `edit_record()`     | Edita registro existente           | `only_required=False`, `submit=True`           |
| `delete_record()`   | Elimina registro y dependencias    | `delete_dependencies=True`                       |
| `validate_record()` | Valida datos en detalle/edición   | -                                                  |

### 🧭 Navegación

| Método                | Descripción                      |
| ---------------------- | --------------------------------- |
| `goto_index_page()`  | Navega al índice del módulo     |
| `goto_create_page()` | Navega al formulario de creación |
| `goto_edit_page()`   | Navega al formulario de edición  |
| `goto_detail_page()` | Navega a la vista de detalle      |

### 📊 Generación de Datos

| Método                          | Descripción                            | Parámetros                                       |
| -------------------------------- | --------------------------------------- | ------------------------------------------------- |
| `generate_random_data()`       | Genera datos para campos y dependencias | `is_edit=False`, `generate_main_fields=False` |
| `create_dependency_instance()` | Crea instancia de dependencia           | `dependency_class`, `mode="create"`           |
| `delete_dependencies()`        | Elimina dependencias creadas            | `mode=None`                                     |

### ✅ Validaciones Específicas

| Método                            | Descripción                                 | Uso                  |
| ---------------------------------- | -------------------------------------------- | -------------------- |
| `validate_create_invalid_data()` | Valida campo con dato inválido en creación | Tests de validación |
| `validate_create_valid_data()`   | Valida campo con dato válido en creación   | Tests de aceptación |
| `validate_edit_invalid_data()`   | Valida campo con dato inválido en edición  | Tests de validación |
| `validate_edit_valid_data()`     | Valida campo con dato válido en edición    | Tests de aceptación |

### 🔍 Búsqueda y Filtros

| Método                                    | Descripción                      |
| ------------------------------------------ | --------------------------------- |
| `search_records_with_filters()`          | Aplica filtros y busca registros  |
| `search_disabled_records_with_filters()` | Busca en registros deshabilitados |
| `validate_filter_on_current_page()`      | Valida filtros en página actual  |

## 🛠️ Utilidades y Herramientas

### 🎲 Generadores de Datos (`utils_functions.py`)

```python
# Generadores básicos
generate_random_string(10)              # "AbCdEfGhIj"
generate_random_int(1, 100)             # 42
generate_random_float(10.0, 99.99)      # "45.67"
generate_random_email()                 # "user@example.com"

# Formateo de fechas
format_date_in_dd_mm_aaaa(datetime.now())    # "28/09/2025"
format_date_in_spanish(datetime.now())       # "28 de septiembre de 2025"
```

### 🛡️ Decorador de Manejo de Errores

```python
def catch_test_failures(func):
    """Decorador que limpia registros automáticamente si hay errores."""
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            if hasattr(self, 'delete_record'):
                await self.delete_record()
            pytest.fail(str(e))
    return wrapper
```

## 🎥 Grabación y Screenshots

### 📹 Configuración Automática

El framework captura automáticamente videos y screenshots cuando `RECORD_SCREEN=true`:

- **Videos**: Solo se guardan si el test falla
- **Screenshots**: Se toman automáticamente en fallos
- **Organización**: Por timestamp y nombre de test

### 🗂️ Estructura de Evidencias

```
tests/media/
├── screenshots/
│   ├── test_create_evento_EVT_01_28_09_25-14_30_45.png
│   └── ...
└── videos/
    ├── test_complete_crud_EVT_01_28_09_25-14_30_45.webm
    └── ...
```

## 🚀 Mejores Prácticas

### ✅ Estructura Recomendada

```python
# 1. Usar Enums para campos
class FieldEventoEnum(Enum):
    TITULO = "title"
    UBICACION = "location"

# 2. Configurar campos como atributos de clase
self.input_field_instances = {
    FieldEventoEnum.TITULO.value: FieldsPage(...),
}

# 3. Tests parametrizados
@pytest.mark.parametrize("field, validate_type", [
    (FieldEventoEnum.TITULO.value, InvalidDataType.REQUIRED),
])

# 4. IDs descriptivos
pytest.param(..., id="EVT_01 CRUD completo evento")
```

### 🎯 Naming Conventions

- **Tests**: `test_complete_crud_operations`
- **IDs**: `EVT_01 Descripción clara`
- **Enums**: `FieldEventoEnum.TITULO`
- **Page Objects**: `PageEventos`

---

## 🔧 Funcionalidades Avanzadas y Customización

### 🚀 Capacidades del Framework

El framework actual soporta una amplia gama de funcionalidades out-of-the-box:

#### ✅ **Funcionalidades Incluidas:**

| Funcionalidad              | Descripción                       | Soporte     |
| -------------------------- | ---------------------------------- | ----------- |
| **Campos Básicos**  | text, number, email, textarea      | ✅ Completo |
| **Selects**          | select, select2, select2 múltiple | ✅ Completo |
| **Fechas y Tiempo**  | date, datetime, time               | ✅ Completo |
| **Checkboxes/Radio** | checkbox, radio buttons            | ✅ Completo |
| **Archivos**         | file upload, image upload          | ✅ Completo |
| **Formsets**         | Django formsets dinámicos         | ✅ Completo |
| **Dependencias**     | Relaciones entre páginas          | ✅ Completo |
| **Validaciones**     | Required, min/max length, patterns | ✅ Completo |
| **CRUD Completo**    | Create, Read, Update, Delete       | ✅ Completo |
| **Filtros**          | Búsqueda y filtrado               | ✅ Completo |

#### 🔄 **Operaciones Automáticas:**

- **Generación de datos** aleatorios por tipo de campo
- **Manejo de errores** con limpieza automática
- **Navegación inteligente** entre páginas
- **Validación cruzada** entre vistas (índice, detalle, edición)
- **Gestión de dependencias** automática
- **Grabación de evidencias** en fallos

### ⚠️ **Limitaciones y Casos Especiales**

#### 🛠️ **¿Qué hacer si una funcionalidad no funciona?**

Si encuentras un caso específico que el framework no maneja automáticamente:

##### 1. **Desarrollar en tu Page Object específico**

```python
class PageEventos(GenericPage):
    def __init__(self, page):
        super().__init__(page, "Eventos", ["Catálogos", "Eventos"])

        # ✅ Selectores como atributos (patrón POM correcto)
        self.calendar_custom_button = 'button[data-calendar="custom"]'
        self.calendar_input = 'input[data-calendar-input]'
        self.calendar_confirm_button = 'button[data-calendar-confirm]'
        self.custom_action_button = 'button[data-custom-action]'

    # ✅ Método custom para caso específico
    async def handle_special_calendar_widget(self):
        """Manejo especial para widget de calendario personalizado."""
        await self.page.click(self.calendar_custom_button)
        await self.page.fill(self.calendar_input, "2025-12-31")
        await self.page.click(self.calendar_confirm_button)

    # ✅ Override de método base si es necesario
    async def create_record(self, only_required=False, validate_record=False):
        """Override para añadir lógica específica antes/después de crear."""
        # Lógica previa específica
        await self.handle_special_calendar_widget()

        # Llamar al método padre
        await super().create_record(only_required, validate_record)

        # Lógica posterior específica
        await self.page.click(self.custom_action_button)
```

##### 2. **Casos que requieren desarrollo custom:**

- **Widgets JavaScript complejos** (calendarios especiales, editores WYSIWYG)
- **Flujos de múltiples pasos** específicos del módulo
- **Validaciones de negocio** únicas
- **Integraciones externas** (APIs, servicios)
- **Componentes React/Vue** embebidos

### 🚨 **REGLAS CRÍTICAS - NO MODIFICAR ARCHIVOS BASE**

#### ❌ **NUNCA modificar estos archivos:**

```
tests/pages/base_pages/
├── base_page.py            ❌ NO TOCAR
├── constants.py            ❌ NO TOCAR
├── fields_page.py          ❌ NO TOCAR
├── generic_page.py         ❌ NO TOCAR
└── standard_django_page.py ❌ NO TOCAR

tests/conftest.py           ❌ NO TOCAR
```

#### ⚡ **¿Por qué NO modificar archivos base?**

1. **Rompe otros módulos**: Los cambios afectan TODOS los Page Objects
2. **Pérdida de funcionalidad**: Puede eliminar características que otros módulos usan
3. **Dificulta mantenimiento**: Los cambios se pierden en actualizaciones
4. **Introduce bugs**: Puede causar fallos en tests existentes
5. **Rompe el patrón**: Viola la arquitectura del framework

#### ✅ **Alternativa correcta - Override en tu Page Object:**

```python
class PageEventos(GenericPage):
    # ✅ CORRECTO: Override específico en tu clase
    async def fill_data(self, data):
        """Override para manejar campo especial antes del llenado normal."""
        # Manejo especial para campo custom
        if "campo_especial" in data:
            await self.handle_custom_field(data["campo_especial"])
            del data["campo_especial"]

        # Llamar método padre para el resto
        await super().fill_data(data)
```

### � **Override de Métodos - Customización Avanzada**

#### 🔄 **Todos los métodos pueden ser sobrescritos:**

Cualquier método de las clases base puede ser customizado en tu Page Object específico:

##### **Métodos CRUD:**

```python
class PageEventos(GenericPage):
    def __init__(self, page):
        super().__init__(page, "Eventos", ["Catálogos", "Eventos"])

        # ✅ Selectores como atributos (patrón POM)
        self.special_confirm_button = 'button[data-special-confirm]'
        self.business_rules_section = '.business-rules-panel'
        self.edit_permission_indicator = '[data-can-edit]'

    # Override método de creación
    async def create_record(self, only_required=False, validate_record=False):
        # Lógica previa específica
        await self.setup_special_conditions()

        # Método padre
        result = await super().create_record(only_required, validate_record)

        # Lógica posterior específica
        await self.verify_business_rules()
        return result

    # Override método de edición
    async def edit_record(self, only_required=False, submit=True):
        # Verificación previa específica
        if not await self.can_edit_current_record():
            pytest.skip("Record cannot be edited due to business rules")

        return await super().edit_record(only_required, submit)

    # Override método de eliminación
    async def delete_record(self, delete_dependencies=True):
        # Confirmación especial para este módulo
        await self.page.click(self.special_confirm_button)

        return await super().delete_record(delete_dependencies)
```

##### **Métodos de Validación:**

```python
class PageEventos(GenericPage):
    # Override validación de datos inválidos
    async def validate_create_invalid_data(self, field, validate_type, error_message=None):
        # Lógica previa para casos especiales
        if field == "fecha_evento" and validate_type == InvalidDataType.REQUIRED:
            # Manejo especial para fecha de evento
            await self.setup_date_validation()

        return await super().validate_create_invalid_data(field, validate_type, error_message)

    # Override validación de registro
    async def validate_record(self):
        # Validaciones específicas del negocio
        await self.validate_event_business_rules()

        # Validación estándar
        return await super().validate_record()
```

##### **Métodos de Navegación:**

```python
class PageEventos(GenericPage):
    # Override navegación al índice
    async def goto_index_page(self):
        # Lógica previa (ej: limpiar filtros específicos)
        await self.clear_special_filters()

        return await super().goto_index_page()

    # Override navegación a creación
    async def goto_create_page(self):
        # Verificar permisos específicos
        if not await self.has_create_permission():
            pytest.skip("User doesn't have create permission")

        return await super().goto_create_page()
```

##### **Métodos de Generación de Datos:**

```python
class PageEventos(GenericPage):
    # Override generación de datos
    async def generate_random_data(self, is_edit=False, generate_main_fields=False):
        # Generar datos base
        data = await super().generate_random_data(is_edit, generate_main_fields)

        # Añadir lógica específica
        if "fecha_evento" in data:
            # Asegurar que fecha de evento sea futura
            data["fecha_evento"] = self.generate_future_date()

        # Añadir validaciones de negocio
        data = await self.apply_business_rules_to_data(data)

        return data
```

#### 🎨 **Patrones de Override Recomendados:**

##### **1. Patrón Wrapper (Más común):**

```python
async def method_override(self, *args, **kwargs):
    # Lógica previa
    await self.pre_method_logic()

    # Método padre
    result = await super().method_override(*args, **kwargs)

    # Lógica posterior
    await self.post_method_logic()

    return result
```

##### **2. Patrón Condicional:**

```python
async def method_override(self, *args, **kwargs):
    if self.special_condition():
        # Implementación completamente custom
        return await self.custom_implementation(*args, **kwargs)
    else:
        # Método padre
        return await super().method_override(*args, **kwargs)
```

##### **3. Patrón de Extensión:**

```python
async def method_override(self, *args, **kwargs):
    # Método padre
    result = await super().method_override(*args, **kwargs)

    # Extensión específica
    result.update(await self.add_specific_functionality())

    return result
```

### 📋 **Guía de Resolución de Problemas**

#### 🔍 **¿Cómo identificar si necesitas override?**

1. **El método base no funciona** para tu caso específico
2. **Necesitas lógica adicional** antes/después de la operación
3. **Validaciones de negocio** específicas del módulo
4. **Widgets o componentes** únicos en tu módulo
5. **Flujos de trabajo** diferentes al estándar

#### ✅ **Checklist antes de hacer override:**

- [ ] ¿Intenté usar configuración de FieldsPage primero?
- [ ] ¿Revisé si existe un InputType que maneje mi caso?
- [ ] ¿Consulté la documentación de constants.py?
- [ ] ¿Es realmente específico de mi módulo?
- [ ] ¿Documenté el override con comentarios claros?

#### 🚀 **Ejemplos de Customización Exitosa:**

```python
class PageReservaciones(GenericPage):
    """Ejemplo de Page Object con múltiples overrides específicos."""

    def __init__(self, page):
        super().__init__(page, "Reservaciones", ["Operaciones", "Reservaciones"])

        # ✅ Selectores como atributos (patrón POM correcto)
        self.reservation_calendar_button = '[data-calendar="reservation"]'
        self.calendar_popup = '.calendar-popup'
        self.availability_indicator = '.room-availability'
        self.confirmation_panel = '.reservation-confirmation'
        self.date_minimum_setter = '[data-min-date-control]'

    async def create_record(self, only_required=False, validate_record=False):
        """Override: Reservaciones requiere verificar disponibilidad."""
        # 1. Verificar disponibilidad antes de crear
        await self.verify_room_availability()

        # 2. Crear reservación
        result = await super().create_record(only_required, validate_record)

        # 3. Enviar confirmación específica
        await self.send_reservation_confirmation()

        return result

    async def validate_create_invalid_data(self, field, validate_type, error_message=None):
        """Override: Validaciones especiales para fechas de reservación."""
        if field == "fecha_entrada" and validate_type == InvalidDataType.MIN_VALUE:
            # Configurar fecha mínima como hoy
            await self.set_minimum_date_to_today()

        return await super().validate_create_invalid_data(field, validate_type, error_message)

    async def handle_custom_calendar_widget(self):
        """Método custom específico para widget de calendario de reservaciones."""
        await self.page.click(self.reservation_calendar_button)
        await self.page.wait_for_selector(self.calendar_popup)
        # ... lógica específica del widget
```

---

## 🎯 **Recordatorio Importante: Patrón POM (Page Object Model)**

### ✅ **SIEMPRE usar selectores como atributos de clase:**

```python
class PageEventos(GenericPage):
    def __init__(self, page):
        super().__init__(page, "Eventos", ["Catálogos", "Eventos"])

        # ✅ CORRECTO: Selectores como atributos
        self.submit_button = 'button[type="submit"]'
        self.cancel_button = '.btn-cancel'
        self.error_message = '.alert-danger'

    async def submit_form(self):
        # ✅ CORRECTO: Usar el atributo
        await self.page.click(self.submit_button)

    async def cancel_action(self):
        # ✅ CORRECTO: Usar el atributo
        await self.page.click(self.cancel_button)
```

### ❌ **NUNCA hardcodear selectores en métodos:**

```python
async def submit_form(self):
    # ❌ MAL: Selector hardcodeado
    await self.page.click('button[type="submit"]')
```

### 🏆 **Beneficios del patrón POM correcto:**

- **Mantenibilidad**: Un solo lugar para cambiar selectores
- **Reutilización**: Los selectores se pueden usar en múltiples métodos
- **Legibilidad**: Nombres descriptivos en lugar de selectores crípticos
- **Testing**: Fácil de mockear y probar

---

**🎯 Resumen: El framework es potente y flexible. Para casos especiales, customiza en tu Page Object específico, nunca modifiques los archivos base. ¡Usa overrides para adaptar cualquier funcionalidad a tus necesidades! Y SIEMPRE sigue el patrón POM con selectores como atributos de clase.**

Al seguir esta estructura y enfoque modular, se garantiza que el código de prueba sea reutilizable y fácil de entender, lo que contribuye a un ciclo de desarrollo ágil y efectivo. Este enfoque no solo promueve la calidad del software, sino que también facilita la colaboración entre los miembros del equipo al proporcionar una base sólida para las pruebas automatizadas.

---

## 🔍 Troubleshooting y FAQ

### 🚨 **Problemas Comunes y Soluciones**

#### 🎭 **Errores de Playwright**

##### ❌ **Error: "Element not found" / "Selector not found"**

**Síntomas:**

```
playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.
=========================== locator.click(...) ===========================
waiting for locator('button[type="submit"]')
```

**Soluciones:**

```python
# ✅ 1. Agregar wait explícito
await self.page.wait_for_selector(self.submit_button)
await self.page.click(self.submit_button)

# ✅ 2. Usar wait_for_load_state
await self.page.wait_for_load_state('networkidle')
await self.page.click(self.submit_button)

# ✅ 3. Verificar visibilidad
await self.page.wait_for_selector(self.submit_button, state='visible')
```

##### ❌ **Error: "Element is not clickable" / "Element is covered"**

**Soluciones:**

```python
# ✅ 1. Scroll al elemento
await self.page.locator(self.submit_button).scroll_into_view_if_needed()
await self.page.click(self.submit_button)

# ✅ 2. Forzar click
await self.page.click(self.submit_button, force=True)

# ✅ 3. Usar JavaScript click
await self.page.evaluate(f'document.querySelector("{self.submit_button}").click()')
```

##### ❌ **Error: "Navigation timeout"**

**Soluciones:**

```python
# ✅ 1. Aumentar timeout específico
await self.page.goto(url, timeout=60000)

# ✅ 2. Wait for specific condition
await self.page.goto(url)
await self.page.wait_for_selector('.main-content')

# ✅ 3. Usar networkidle
await self.page.goto(url, wait_until='networkidle')
```

#### 🔧 **Problemas de Framework**

##### ❌ **Error: "AttributeError: 'PageEventos' object has no attribute 'field_name'"**

**Causa:** Campo no configurado en `input_field_instances`

**Solución:**

```python
class PageEventos(GenericPage):
    def __init__(self, page):
        super().__init__(page, "Eventos", ["Catálogos", "Eventos"])

        # ✅ Asegurar que todos los campos estén configurados
        self.input_field_instances = {
            "titulo": FieldsPage(...),
            "ubicacion": FieldsPage(...),
            # Agregar el campo faltante
            "campo_faltante": FieldsPage(...),
        }
```

##### ❌ **Error: "generate_random_data failed" / Datos no válidos**

**Soluciones:**

```python
# ✅ 1. Verificar configuración de campo
FieldsPage(
    page=page,
    name="email",
    field_selector='input[name="email"]',
    input_type=InputType.EMAIL,  # ✅ Tipo correcto
    required=True
)

# ✅ 2. Override para casos especiales
async def generate_random_data(self, is_edit=False, generate_main_fields=False):
    data = await super().generate_random_data(is_edit, generate_main_fields)

    # Ajustar datos específicos
    if "fecha_evento" in data:
        data["fecha_evento"] = self.generate_future_date()

    return data
```

##### ❌ **Error: "Dependency creation failed"**

**Solución:**

```python
# ✅ Verificar configuración de dependencias
self.input_field_dependencies = {
    PageUsuarios: {
        DependencyAction.CREATE: {
            "responsable": ["nombres", " ", "apellido_paterno"]
        },
        # ✅ Agregar acción DELETE si es necesaria
        DependencyAction.DELETE: {}
    }
}
```

#### 🎥 **Problemas de Grabación**

##### ❌ **Videos no se graban o son corruptos**

**Soluciones:**

```python
# ✅ 1. Verificar configuración en conftest.py
@pytest.fixture
async def browser_context(browser):
    context = await browser.new_context(
        record_video_dir="media/videos/" if RECORD_SCREEN else None,
        record_video_size={"width": 1280, "height": 720}  # ✅ Tamaño fijo
    )
```

##### ❌ **Screenshots no se toman en fallos**

**Verificar:**

```python
# ✅ En conftest.py debe estar configurado
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # ... configuración de screenshot automático
```

### 🔧 **Comandos de Diagnóstico**

#### **Debug de Tests:**

```bash
# Ejecutar con debug detallado
pytest -s -v --tb=long tests/e2e/catalogos/test_eventos.py

# Ejecutar un test específico con output completo
pytest -s -v -k "test_create_record" --capture=no

# Ver todos los prints y logs
pytest -s --log-cli-level=DEBUG
```

#### **Debug de Playwright:**

```bash
# Ejecutar en modo headed (con browser visible)
HEADLESS_MODE=false pytest tests/e2e/catalogos/test_eventos.py

# Debug con inspector de Playwright
PWDEBUG=1 pytest tests/e2e/catalogos/test_eventos.py

# Slow motion para ver acciones
SLOW_MO=2000 pytest tests/e2e/catalogos/test_eventos.py
```

### ❓ **FAQ Frecuentes**

#### **P: ¿Por qué mi test falla aleatoriamente?**

**R:** Problemas de timing. Agregar waits explícitos:

```python
await self.page.wait_for_load_state('networkidle')
await self.page.wait_for_selector(selector, state='visible')
```

#### **P: ¿Cómo debuggear un selector que no funciona?**

**R:** Usar inspector de Playwright:

```python
# Pausar ejecución para inspeccionar
await self.page.pause()

# O verificar si existe
element = await self.page.query_selector(selector)
print(f"Element found: {element is not None}")
```

#### **P: ¿Cómo manejar elementos que aparecen dinámicamente?**

**R:** Usar waits condicionales:

```python
# Esperar que aparezca
await self.page.wait_for_selector('.dynamic-element')

# O esperar que desaparezca
await self.page.wait_for_selector('.loading-spinner', state='hidden')
```

#### **P: ¿Por qué GenericPage no encuentra mi campo?**

**R:** Verificar configuración en `input_field_instances`:

```python
# El nombre del campo debe coincidir exactamente
self.input_field_instances = {
    "titulo": FieldsPage(...),  # ✅ Debe coincidir con name="titulo"
}
```
