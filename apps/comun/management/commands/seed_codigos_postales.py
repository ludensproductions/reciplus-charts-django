import json
import os
import time

from django.core.management.base import BaseCommand
from simple_history.utils import bulk_create_with_history

from apps.users.models import CodigoPostal, Municipio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    help = "Seed database with postal codes"

    def handle(self, *args, **kwargs):
        seed_codigos_postales()
        self.stdout.write(self.style.SUCCESS("Seeded postal codes successfully"))


def seed_codigos_postales():
    # Count time
    start = time.time()
    f = open(f"{BASE_DIR}/commands/json/codigos_postales.json", "r", encoding="utf-8")
    json_array = json.load(f)

    municipios_exist = Municipio.objects.all().exists()

    if municipios_exist:
        return

    for item in json_array:
        municipios = item["ciudad_municipio"]
        codigos_postales = item["codigos"]

        # Asumimos que el municipio ya existe, y lo buscamos
        for municipio_name in set(municipios):  # Evita duplicados
            municipio = Municipio.objects.filter(municipio=municipio_name).first()
            # Crear instancias de CodigoPostal
            if municipio:
                codigos_bulk = []
                for codigo_postal in set(codigos_postales):
                    # Verificar si ya existe el código postal para ese municipio
                    # if not CodigoPostal.objects.filter(municipio=municipio, codigo_postal=codigo_postal).exists():
                    codigos_bulk.append(CodigoPostal(municipio=municipio, codigo_postal=codigo_postal))

                # Bulk create para los códigos postales
                bulk_create_with_history(codigos_bulk, CodigoPostal, ignore_conflicts=True)
                # CodigoPostal.objects.bulk_create(codigos_bulk, ignore_conflicts=True)

    print(f"Tiempo de ejecución: {time.time() - start} segundos")
