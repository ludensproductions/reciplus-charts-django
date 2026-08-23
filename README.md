# Django template

## Introduction

A comprehensive Django project template with modern tooling and multiple pre-configured apps.

> If you are reading this on VSCode, it is recommended to use **`CTRL + SHIFT + P`** and search for the option of **`Markdown: Open Preview`**, you could also read this file on **`github.com`**

Provide a solid foundation for Django-based systems, including common modules, consistent settings, and pre-integrated tools for development and testing.

Developers and teams seeking a standardized, production-ready Django project structure.

## Content

- [Django template](#django-template)
  - [Introduction](#introduction)
  - [Content](#content)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Quickstart](#2-quickstart)
    - [Unix instructions](#unix-instructions)
    - [Windows instructions](#windows-instructions)
  - [3. Usage](#3-usage)
    - [3.1. Run the project with daphne](#31-run-the-project-with-daphne)
    - [3.2. Internationalization (i18n)](#32-internationalization-i18n)
    - [3.3. How to run Gotenberg](#33-how-to-run-gotenberg)
  - [4. Additional considerations](#4-additional-considerations)
    - [4.1. Configuring hooks](#41-configuring-hooks)
  - [5. Support](#5-support)
    - [5.1 Frecuently asks questions](#51-frecuently-asks-questions)
      - [1. How do I install a new requirement to the project?](#1-how-do-i-install-a-new-requirement-to-the-project)

## 1. Prerequisites

- Python 3.11+
- Docker

## 2. Quickstart

### Unix instructions

```rb
git clone https://github.com/ludensproductions/django-template.git
cd django-template
cp .env.example .env
uv venv venv
. venv/bin/activate
uv pip install -r requirements.txt
prek install
docker compose up -d
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Windows instructions

```rb
git clone https://github.com/ludensproductions/django-template.git
cd django-template
cp .env.example .env
uv venv venv
.\venv\Scripts\activate
uv pip install -r requirements.txt
prek install
docker compose up -d
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 3. Usage

```rb
# 1. Run the migrations:
python manage.py makemigrations
python manage.py migrate

# 2. Create superuser:
python manage.py createsuperuser

# 3. Make sure your virtual environment is active
prek install

# 4. Run the server:
python manage.py runserver
```

### 3.1. Run the project with daphne

After completing the setup steps above, you can run the project with Daphne depending on the environment.

#### Development

For local development with `DEBUG=True`, `collectstatic` is not required.

```rb
daphne djangoproject.asgi:application
```

#### Production

For production or any environment using `DEBUG=False`, make sure `DEBUG=False`, `WEB_URL`, and `ALLOWED_HOSTS` are configured correctly in your `.env`, then build local optimized static files before starting Daphne.

```rb
python manage.py collectminifiedstatic
daphne djangoproject.asgi:application
```

`collectminifiedstatic` runs `collectstatic`, downloads supported external CSS and JS assets into local static output, rewrites supported references to those local files, and minifies the collected assets for deployment.

> To change port just use the -p flag, for instance `daphne djangoproject.asgi:application -p 3000`

### 3.2. Internationalization (i18n)

Use `makemessages` to generate or update translation files, and `compilemessages` to compile them.

```rb
# Generate/update messages for English
python manage.py makemessages -l en -i venv -i .venv -i env -i node_modules -i static -i media -i tests

# Generate/update messages for Spanish (Mexico)
python manage.py makemessages -l es_MX -i venv -i .venv -i env -i node_modules -i static -i media -i tests

# Compile all messages
python manage.py compilemessages
```

Use `-l` depending on the language you want to translate.

You can download it from here: https://www.gnu.org/software/gettext/

### 3.3. How to run Gotenberg

To run Gotenberg you just need to use the following command.

```rb
docker compose -f gotenberg.compose.yaml up -d
```

## 4. Additional considerations

### 4.1. Configuring hooks

After cloning the repository, make sure to activate your virtual environment first, then install prek and configure the hooks by running:

```rb
# Make sure your virtual environment is active
prek install
```

This will set up git hooks that:

- Check formatting and code style of files before pushing
- Ensure .env variables required in [.env.example](.env.example) are present (this check always runs)
- Block commits that don't meet quality standards

For better visibility of prek check details, it's recommended to make commits using the terminal instead of a GUI git client.

## 5. Support

For issues and feature requests, please contact PMO or PO.

If you need direct assistance, please contact the maintainers through the internal communication channels defined by your team.

### 5.1 Frecuently asks questions

#### 1. How do I install a new requirement to the project?

Once the library is installed, it will be necessary to _**write the version that was installed in the requirements.txt**_.

- Run the **`pip freeze`** command and copy the version manually into **`requirements.project.txt`**.
    > **Note:** Please do not copy all new libraries. Only the libraries explicitly installed with pip install should be copied; do not include copying the sub-libraries installed by the newly added library.
- Search for the library at [https://pypi.org/](https://pypi.org/project/) and copy the latest version from there (example: <https://pypi.org/project/django-q/#history>).
- You can see the output of the terminal at the time it was installed and get the version from there.
