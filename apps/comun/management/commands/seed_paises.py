import json
import os
import time

from django.core.management.base import BaseCommand
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from simple_history.utils import bulk_create_with_history

from apps.users.models import Estado, Municipio, Pais, User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_ADMIN = User.objects.get(username="admin")


class Command(BaseCommand):
    """Seed database with countries, states, and cities from a JSON file."""

    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        """Seed countries, states, and cities into the database."""
        seed_cities(self)
        self.stdout.write(self.style.SUCCESS(str(_("Ciudades cargadas correctamente"))))


def seed_cities(self):
    """Load countries, states, and cities from JSON sources.

    Side Effects:
        Creates Pais, Estado, and Municipio records when none exist.
    """
    # Track execution time.
    start = time.time()
    file_countries_states_cities = open(
        f"{BASE_DIR}/commands/json/countries+states+cities.json", "r", encoding="utf-8"
    )
    json_countries = json.load(file_countries_states_cities)

    paises_exist = Pais.objects.all().exists()
    estados_exist = Estado.objects.all().exists()
    municipios_exist = Municipio.objects.all().exists()

    # ciudades_dict = {}

    # for item in json_codigos_postales:
    #     for ciudad, codigo in zip(item["ciudad_municipio"], item["codigos"]):
    #         if ciudad not in ciudades_dict:
    #             ciudades_dict[ciudad] = set()
    #         ciudades_dict[ciudad].add(codigo)

    if not paises_exist and not estados_exist and not municipios_exist:
        self.stdout.write(str(_("No hay registros de paises, estados y municipios")))
        self.stdout.write(str(_("Insertando paises y estados...")))
        paises_entries = {}
        estados_entries = {}
        municipios_entries = []
        # codigos_postales = []

        for item in json_countries:
            # Phase 1: Create or retrieve Pais
            country = item["name"]
            code = item["iso3"]
            if code not in paises_entries:
                paises_entries[code] = Pais(
                    pais=country,
                    clave=code,
                    created_by=USER_ADMIN,
                )

            pais_obj = paises_entries[code]

            # Phase 2: Create or retrieve Estado
            if item["states"]:
                for states in item["states"]:
                    state = states["name"]
                    state_code = states["state_code"]
                    estado_key = f"{code}_{state_code}"

                    if estado_key not in estados_entries:
                        estados_entries[estado_key] = Estado(
                            clave=state_code,
                            estado=state,
                            pais=pais_obj,  # Link to the Pais object
                            created_by=USER_ADMIN,
                        )

                    estado_obj = estados_entries[estado_key]

                    # Phase 3: Create Municipio
                    if states["cities"]:
                        for city in states["cities"]:
                            municipio_obj = Municipio(
                                clave=city["id"],
                                municipio=city["name"],
                                estado=estado_obj,  # Link to the Estado object
                                created_by=USER_ADMIN,
                            )

                            municipios_entries.append(municipio_obj)

                            # if not country == "Mexico":
                            #     continue

                            # codigos_cp = list(ciudades_dict.get(city['name'], []))

                            # for codigo_cp in codigos_cp:
                            #     codigos_postales.append(CodigoPostal(
                            #         municipio=municipio_obj,
                            #         codigo_postal=codigo_cp,
                            #         created_by=USER_ADMIN,
                            #     ))

                    else:
                        # If no cities, use the state name as the city

                        municipios_entries.append(
                            Municipio(
                                clave=0,
                                municipio=estado_obj.estado,
                                estado=estado_obj,
                                created_by=USER_ADMIN,
                            )
                        )

            else:
                # If no states, use the country name as the state and city
                estado_key = f"{code}_default"
                if estado_key not in estados_entries:
                    estados_entries[estado_key] = Estado(
                        clave=code,
                        estado=country,
                        pais=pais_obj,
                        created_by=USER_ADMIN,
                    )

                estado_obj = estados_entries[estado_key]
                municipios_entries.append(
                    Municipio(
                        clave=0,
                        municipio=country,
                        estado=estado_obj,
                        created_by=USER_ADMIN,
                    )
                )

        self.stdout.write(str(_("Insertando paises")))
        bulk_create_with_history(paises_entries.values(), Pais)
        self.stdout.write(str(_("Paises insertados correctamente")))

        self.stdout.write(str(_("Insertando estados")))
        bulk_create_with_history(estados_entries.values(), Estado)
        self.stdout.write(str(_("Estados insertados correctamente")))

        self.stdout.write(str(_("Insertando municipios")))
        bulk_create_with_history(municipios_entries, Municipio)
        self.stdout.write(str(_("Municipios insertados correctamente")))

        # self.stdout.write("Insertando codigos postales")
        # bulk_create_with_history(codigos_postales, CodigoPostal)
        # self.stdout.write("Codigos postales insertados correctamente")

        self.stdout.write(str(_("Paises, estados y municipios insertados correctamente")))
        self.stdout.write(str(format_lazy(_("Tiempo de ejecucion: {seconds} segundos"), seconds=time.time() - start)))
