#!/bin/bash

# Instalar dependencias nuevas
pip install -r ./requirements.project.txt

# run cluster
python manage.py qcluster
