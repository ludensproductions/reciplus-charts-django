# EIU Generator

Este repositorio contiene una plantilla de automatización para la generación de archivos EIU, la cual utiliza **Playwright** con **pytest** como framework de pruebas para Django, para así obtener los elementos de los URLs y comprimirlos dentro de un archivo Word con el formato de un EIU. A continuación, se describen los pasos para instalar y configurar el entorno de desarrollo, así como las instrucciones para ejecutar las pruebas.

<br>

## Prerrequisitos

Antes de comenzar, asegúrate de tener lo siguiente instalado:

- **Python 3.11 o mayor**: Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **Git**: Para clonar el repositorio. Puedes descargarlo desde [git-scm.com](https://git-scm.com/).

**Obtener los enlaces necesarios para generar el EIU**

- Instalar la libreria django-urlconf-export en el proyecto del cual se quiere generar el EIU con el comando:

```bash
pip install django-urlconf-export
```

- En installed apps en settings agregar "django_urlconf_export":

```
INSTALLED_APPS = [
    "django_urlconf_export"
]
```

- Ejecutar el comando:

```bash
python manage.py export_urlconf_to_file > "urlconf.json"
```

El JSON generado se debera ver algo asi:

```json
[{"route": "admin/", "includes": [{"route": "", "name": "index"},
 {"route": "login/", "name": "login"}, {"route": "logout/", "name": "logout"}, {"route": "password_change/", "name": "password_change"},
 {"route": "password_change/done/", "name": "password_change_done"},
 {"route": "autocomplete/", "name": "autocomplete"},
 {"route": "jsi18n/", "name": "jsi18n"},
 {"route": "r/<int:content_type_id>/<path:object_id>/", "name": "view_on_site"},
]
```

**Ahora se puede proceder con la sección "Uso del sistema".**

<br>

## Estructura del proyecto

```bash
tu-repo/
│
├──test
│	├──e2e
│	│    ├── eiu_generator/                  # Carpeta principal del generador de EIUs
│	│    │   ├── eiu_word/                   # Directorio donde se genera el EIU generado
│	│    │   ├── urls_json/                  # Carpeta donde se encuentran los archivos json
│	│    │   ├──── fixed_urls.json           # Json con el formato arreglado de las URLs
│	│    │   ├──── omit.json                 # Json con el atributo title de los elementos que requieren ser ignorados
│	│    │   ├──── urls.json                 # Json con el formato erroneo de las URLs (generalmente generado por un admin o el Sami)
│	│    │   ├── utils/                      # Carpeta donde se genera el reporte y configuración del code coverage (No tocar)
│	│    │   ├──── eiu_generator_utils.py    # Archivo que contiene metodos que utiliza test_prueba_EIU.py
│	│    │   ├── parse_urls.py               # Algoritmo que toma el archivo urls.json, y genera un formato valido para los urls en el archivo fixed_urls.json
│	│    │   └── README.md                   # Documentación del proyecto
│	│    │   ├── generate_eiu.py          # Archivo que contiene el algoritmo para generar un Json que se utiliza para generar el archivo word
│	│    │   ├── word_eiu.py                 # Archivo que contiene el algoritmo para generar el archivo word
```

<br>

## Instalación

### 1. Configuración de variables de entorno (.env)

En la raíz del proyecto se encontrará un archivo *.env.example*, el cual se deberá de copiar y pegar para renombrarlo como *.env*

Este archivo servirá para la configuración de las siguientes variables de entorno:

```bash
URL_PROYECTO=http://127.0.0.1:8000/
USER_ADMIN=admin
PASSWORD_ADMIN=12345
```

Durante el transcurso del proyecto se estará actualizando con parámetros que se utilicen continuamente para hacerlo más accesible. Ahora será necesario llevar a cabo los pasos del punto #2 o #3 dependiendo del sistema operativo que utilices para configurar el proyecto en tu máquina local:

### 2. Instalación en Unix (MacOS/Linux)

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
playwright install
```

### 3. Instalación en Windows

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

### 4. Ejecución de las pruebas

Para ejecutar el generador de eius, simplemente se debe utilizar el comando *pytest* desde la línea de comandos en el directorio `/tests/e2e/eiu_generator`. Este comando buscará automáticamente todos los archivos que comiencen con test_ o que terminen con _test.py y ejecutará las pruebas definidas en ellos.

```bash
pytest
```

## Uso del sistema

### Pasos para generar un EIU

1. Navegar a la carpeta eiu_generator
2. Ejecutar los comandos:

```py
python parse_urls.py
pytest generate_eiu.py
python word_eiu.py
```

**Nota: El archivo parse_urls.py leera los links del JSON previamente generado en los prerrequisitos.**

### Consideraciones importantes

Este template, en su mayoría, ya se encuentra totalmente automatizado para generar los EIUs al obtener las URLs correctas del sistema; solo tiene que tomarse en cuenta el archivo omit.json para saber qué elementos serán ignorados para el EIU.
No se tomara en cuenta para el EIU los modulos que tengan una funcionalidad con un gran nivel de complejidad.

### Atributos necesarios para el correcto funcionamiento de la herramienta

Para el correcto funcionamiento del generador de EUIs es necesario que el proyecto siga los estandares de desarrollo.
La herramienta utiliza los atributos title, id y placeholder por lo que es necesario que estos atributos esten omologados en el sistema del cual se generara el EIU.
En el caso de los botones de habilitar, para los elementos "input" que se encuentran en el index del catalogo es necesario que cuenten con el title "Habilitado" mientras que los elementos "a" que se encuentran en las pantallas de habilitar el title del elemento debe de ser "Habilitar".
Ejemplos de atributos:
title="Detalle"

```
title="Detalle"
title="Editar"
title="Eliminar"
<input title="Habilitado">
<a title="Habilitar
placeholder="Usuario"
```

### URLs Json

Una vez el administrador proporcione el json con los urls, al momento de correr el archivo parse_urls.py generara un archivo json con el siguiente formato:

```
[
    "catalogos",
    "catalogos/peliculas",
    "catalogos/peliculas/create",
    "catalogos/peliculas/edit/1",
    "catalogos/peliculas/detail/1",
    "catalogos/albums",
    "catalogos/albums/create",
    "catalogos/albums/edit/1"
]
```

### En caso de errores

Se recomienda contactar con un dev intermediate en caso de errores. Toma en cuenta que el sistema necesita una página válida para generar el sistema, así que asegúrate de revisar los URLs para no estar enviando por error el URL de alguna API en lugar de una página.
