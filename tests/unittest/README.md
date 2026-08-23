# Playwright + Pytest Automation Template for Unit Tests

Este repositorio contiene una plantilla de automatización de pruebas, el cual utiliza **Playwright** con **pytest** como framework de pruebas para Django. A continuación, se describen los pasos para instalar y configurar el entorno de desarrollo, así como las instrucciones para ejecutar las pruebas.

<br>

## Prerrequisitos

Antes de comenzar, asegúrate de tener lo siguiente instalado:

- **Python 3.11 o mayor**: Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **Git**: Para clonar el repositorio. Puedes descargarlo desde [git-scm.com](https://git-scm.com/).

<br>

## Estructura del proyecto

```bash
tu-repo/
│
├── unittest/                   # Carpeta principal de pruebas
│   ├── fixtures/            # Archivos de configuración y fixtures de pytest
│   ├── htmlcov/             # Carpeta donde se genera el reporte y configuración del code coverage (No tocar)
│   ├── pages/               # Page objects, donde se generan los archivos Page de cada módulo para aplicar el patrón de diseño POM
│   ├── report/              # Carpeta donde se genera el reporte HTML una vez ejecutadas las pruebas
│   ├── tests/               # Carpeta donde se generan los archivos tests para pruebas unitarias
│   ├── utils/               # Utilidades y helpers para las pruebas
│   ├── .coverage            # Archivo de configuración para el code coverage (No tocar)
│   ├── .env                 # Variables de entorno
│   ├── .env.example         # Archivo donde se dejan las variables dentorno de ejemplo
│   ├── .gitignore           # Archivo git para incluir las carpetas o archivos que no se subirán al repositorio
│   ├── conftest.py          # Configuración de pytest (No tocar)
│   ├── pytest.ini           # Configuración de pytest (No mover sin autorización)
│   ├── requirements.txt     # Dependencias del proyecto
│   └── README.md            # Documentación del proyecto
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

Durante el transcurso del proyecto se estará actualizando con parámetros que se utilicen continuamente para hacerlo más accesible.Ahora será necesario llevar a cabo los pasos del punto #2 o #3 dependiendo del sistema operativo que utilices para configurar el proyecto en tu máquina local:

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

Para ejecutar las pruebas automatizadas, simplemente se debe utilizar el comando *pytest* desde la línea de comandos en el directorio `/tests`. Este comando buscará automáticamente todos los archivos que comiencen con test_ o que terminen con _test.py y ejecutará las pruebas definidas en ellos.

```bash
pytest
```

#### Alternativas de ejecución

1. Ejecución de un archivo de pruebas en específico (Ejecutará todas las pruebas de ese archivo)

```bash
pytest -k test_example.py
```

2. Ejecución de un caso de prueba con un ID en específico (Ejecutará solo la prueba que contenga ese ID en la función *pytest.param*)

```bash
pytest -k EXAMPLE_04
```

3. Ejecución de una función de pruebas en específico (Ejecutará los casos de prueba que estén incluídos en la función en específico)

```bash
pytest -k test_delete_example
```

**Una vez ejecutadas las pruebas se generará un reporte en HTML propio de pytest con la ruta `tests/report/report.html`**

## Uso del template

### 1. Configuración de archivos Page:

> **Nota:** **Ver archivo Page de ejemplo en `tests/page/page_peliculas.py`, este archivo contiene un ejemplo de la clase Page del módulo de ejemplo automatizado, cumpliendo con todos los pasos a explicar a continuación.**

El **patrón de diseño _Page Object Model (POM)_** se utiliza para estructurar la lógica de interacción con las diferentes páginas de la aplicación, facilitando el mantenimiento y la reutilización del código.

#### Clases base: **BasePage** y **StandardDjangoPage**

Este template incluye dos clases base predefinidas, **BasePage** y **StandardDjangoPage**, las cuales están diseñadas para agilizar el flujo de automatización:

- **BasePage**: Proporciona funcionalidades comunes derivadas de funciones de Playwright, las cuales han sido adaptadas para una mejor implementación en los proyectos. Por ejemplo, se agrega funcionalidad extra a métodos como `wait_for_selector`, o se ofrece la capacidad de remover el atributo `required` del frontend.
- **StandardDjangoPage**: Ofrece funcionalidades específicas generadas para ser utilizadas en proyectos que sigan nuestros estándares de desarrollo definidos en el template de Django. El método `fill_data` recibe un diccionario con los selectores y valores, los cuales son posteriormente iterados sobre cada campo para llenar los formularios, independientemente del tipo de campo que se esté completando.

> **Nota:** Para entender la explicación se recomienda primero analizar los archivos `tests/pages/base_page.py` y `tests/pages/standard_page.py`, los cuales contienen los métodos comentados de respectivas clases con ejemplos incluídos para su uso.

Para crear el archivo Page Object del módulo a automatizar, se debe definir una clase llamada Page que encapsule toda la información específica de ese módulo. Cada una de las clases Page generadas debe heredar de las clases BasePage y StandardDjangoPage de la siguiente manera:

```python
class PagePeliculas(BasePage, StandardDjangoPage):
```

Además, se debe implementar el método constructor ***'init'***, donde se declararán los selectores y mensajes de la interfaz del módulo a automatizar, utilizando nombres descriptivos para cada uno de ellos. *Ver ejemplo en el archivo `tests/pages/peliculas_page.py`*

Una vez declarados los selectores, puedes comenzar a implementar los métodos de interacción con la interfaz del módulo. Para utilizar los métodos de la clase StandardDjangoPage, es necesario trabajar con tres tipos de diccionarios:

1. data: Diccionario que contiene los selectores ya declarados junto con los valores que se intentarán ingresar en cada campo. Este diccionario se utiliza comúnmente para generar formularios automáticamente.
2. data_validate: Diccionario que proporciona los selectores, pero en este caso se refiere a la información que se validará del registro ya realizado, ya sea desde un módulo de detalles o desde el módulo de edición para confirmar que la información se registró correctamente.
3. data_filters: Diccionario que proporciona los selectores del módulo de filtros y los valores de los campos a filtrar, permitiendo realizar búsquedas específicas en los registros con los que se desea interactuar.

Estos diccionarios a utilizar obligatoriamente siempre tienen que venir documentados a nivel clase **Page** (*Ver ejemplo en el archivo `tests/pages/peliculas_page.py`*) Esto indicando los selectores específicos para cada uno de los diccionarios para que las personas que necesiten utilizar métodos de esta clase puedan conocer la estructura de la información.

El siguiente ejemplo ilustra cómo utilizar alguno de estos diccionarios, una vez que los selectores necesarios han sido declarados en el método constructor de la clase Page:

```python
from pages.page_peliculas import PagePeliculas # Se importa la clase del módulo

peliculas_page = PagePeliculas(page) # Se inicializa la clase como peliculas_page

    data = {
        peliculas_page.title_input_selector: 'str_random',      # Selector con su respectivo valor a ingresar
        peliculas_page.year_input_selector: "1999",             # Selector con su respectivo valor a ingresar
        peliculas_page.genre_input_selector: 'str_random',      # Selector con su respectivo valor a ingresar
        peliculas_page.precio_input_selector: 'str_random',     # Selector con su respectivo valor a ingresar
        peliculas_page.sinopsis_input_selector: 'str_random'    # Selector con su respectivo valor a ingresar
    }
```

Una vez configurado lo anterior, es posible invocar métodos de la clase StandardDjangoPage, como por ejemplo fill_data, y pasarle únicamente el diccionario data. El método se encargará automáticamente de rellenar toda la información proporcionada.

**Es obligatorio que todos los métodos de la clase ***Page*** estén totalmente documentados como tipo docstring para que se pueda conocer el próposito de cada uno de ellos, incluyendo la información que recibe y la información que regresa (si aplica).**

> **Nota:** Encontrarás archivos predefinidos como `tests/pages/login_page.py`, que incluye métodos comunes para el inicio y cierre de sesión. Estos métodos pueden ser reutilizados globalmente en tus pruebas, simplemente pasando las credenciales necesarias.

### 2. Configuración de archivos Utils

> **Nota:** **Ver archivo de ejemplo en `tests/utils/utils_example.py`. Este archivo contiene un ejemplo de la clase Page del módulo automatizado, cumpliendo con todos los pasos a explicar a continuación.**

El módulo *utils* contiene funciones auxiliares diseñadas para facilitar y estandarizar utilidades que se pueden utilizar a lo largo de los Page Objects y las pruebas. Este enfoque modular promueve la reutilización del código y mejora la legibilidad.

Comúnmente, en este módulo es donde se generarán los diccionarios de información a utilizar para los métodos de la clase ***StandardDjangoPage***, tales como *data, data_validate y data_filters.*

Se generará un archivo *utils* por cada módulo a automatizar. Es decir, cuando exista un archivo *page*, deberá existir un archivo *utils*. En este módulo se inicializará la clase del módulo a automatizar para poder acceder a los selectores necesarios y construir los diccionarios que se utilizarán en las pruebas.

#### Consideraciones

- Modularidad: Este enfoque modular permite que las funciones en el módulo *utils* sean reutilizadas en diferentes partes del código, evitando la duplicación y mejorando la mantenibilidad.
- Documentación: Es importante documentar cada función en el módulo *utils* con **docstrings** para asegurar que otros desarrolladores comprendan su propósito y uso.

### 3. Configuración de archivos Tests

> **Nota:** **Ver archivo de ejemplo en `tests/e2e/test_example.py`. Este archivo contiene un ejemplo de la clase Page del módulo automatizado, cumpliendo con todos los pasos a explicar a continuación.**

En este módulo es donde la información generada anteriormente es recopilada para llevar a cabo la automatización de las pruebas con ***pytest***

En este archivo se incluyen las importaciones de los módulos generados de Page y Utils, que se utilizan para generar N cantidad de casos de prueba automatizados y la estructura de cada uno de ellos es la siguiente:

```python
@pytest.mark.parametrize("user, password", [
    pytest.param(user_administrador, user_admin_password, id="EXAMPLE_01 Este caso de prueba tiene como propósito que el usuario pueda agregar un registro."),
])
@pytest.mark.asyncio
async def test_create_example(page, user, password):
    login_page = LoginPage(page)
    peliculas_page = PagePeliculas(page)

    data, data_validate, data_filters = await utils_example.generate_random_peliculas_data(page)

    await login_page.login(user, password)

    await peliculas_page.create_pelicula_register(data)

    await peliculas_page.validate_peliculas_register(data_filters, data_validate)
```

- **@pytest.mark.parametrize:** Es un decorador en pytest se utiliza para parametrizar las pruebas, permitiendo que una misma función de prueba se ejecute con diferentes conjuntos de datos de entrada. Esto es útil para evitar la duplicación de código y para probar múltiples escenarios de manera eficiente. En el caso de ejemplo se están incluyendo dos variables generales que son *user* y *password*.
- **pytest.param:** La función pytest.param se utiliza en combinación con @pytest.mark.parametrize para proporcionar un conjunto específico de parámetros para una prueba, junto con un identificador opcional que describe el propósito de ese conjunto de datos. Esto nos permite poder ejecutar N cantidad de casos de prueba en el mismo método controlandolo por las variables proporcionadas, es decir, tomando en cuenta el ejemplo anterior si repito 3 veces la función pytest.param en la cual cambie los valores de las variables *user_administrador* y *user_admin_password* en cada una de los 3, se ejecutará la prueba 3 veces con un usuario diferente cada prueba. Esta es la utilidad de esta función la cual permite ahorrar código en la ejecución de pruebas repetitivas (como en este caso) y poder ingresar un parámetro ***id*** que nos permite ingresar el identificador del caso de prueba y la descripción del caso para identificarlo correctamente.
- **@pytest.mark.asyncio:** Decorador que indica que se está utilizando pytest de forma asíncrona.
- **@pytest.mark.django_db:** Decorador que se utiliza exclusivamente para realizar casos de prueba con comunicación a base de datos (en caso de no requerir no utilizarlo).

Este módulo es fundamental para la automatización de pruebas, ya que permite la ejecución eficiente de múltiples casos de prueba utilizando conjuntos de datos parametrizados. La implementación de decoradores como @pytest.mark.parametrize y @pytest.mark.asyncio optimiza el proceso de prueba, facilitando la creación de pruebas escalables y mantenibles. Además, la utilización de pytest.param permite una identificación clara de cada caso de prueba, mejorando la documentación y el seguimiento de los resultados durante la ejecución.

Al seguir esta estructura y enfoque modular, se garantiza que el código de prueba sea reutilizable y fácil de entender, lo que contribuye a un ciclo de desarrollo ágil y efectivo. Este enfoque no solo promueve la calidad del software, sino que también facilita la colaboración entre los miembros del equipo al proporcionar una base sólida para las pruebas automatizadas.
