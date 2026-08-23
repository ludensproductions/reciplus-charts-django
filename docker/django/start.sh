#!/bin/bash

# Instalar dependencias nuevas
pip install -r ./requirements.txt

# run django server
python manage.py runserver 0.0.0.0:8000 --noreload
