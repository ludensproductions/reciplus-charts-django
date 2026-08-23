import json
import re
from pathlib import Path


def generate_route_strings(data, parent_route=""):
    route_strings = []
    for item in data:
        if isinstance(item, dict) and "route" in item:
            current_route = f"{parent_route}{item['route']}".rstrip("/")

            current_route = re.sub(r"<int:pk>", "1", current_route)
            if "toggle" not in current_route:
                if current_route:
                    route_strings.append(current_route)

                if "includes" in item:
                    route_strings.extend(generate_route_strings(item["includes"], current_route + "/"))
    return route_strings


path_urls = Path(__file__).parent.resolve() / "urls_json" / "urls.json"
try:
    with open(path_urls, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"El archivo {path_urls} no se encuentra.")
    data = []
except json.JSONDecodeError:
    print("Error al decodificar el archivo JSON.")
    data = []

route_strings = generate_route_strings(data)

processed_routes = [re.sub(r"<int:pk>", "1", route) for route in route_strings]

seen_routes = set()
unique_route_strings = []
for route in processed_routes:
    if route not in seen_routes:
        unique_route_strings.append(route)
        seen_routes.add(route)

route_strings_json = json.dumps(unique_route_strings, indent=4)
path_fixed_urls = Path(__file__).parent.resolve() / "urls_json" / "fixed_urls.json"
with open(path_fixed_urls, "w") as file:
    file.write(route_strings_json)

print(f"Las rutas únicas han sido guardadas en {path_fixed_urls}")
