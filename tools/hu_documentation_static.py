"""Static analysis tool to generate HU -> Views documentation.

This script does not load Django and uses AST to inspect `apps/*/views.py`.
"""
import ast
import json
import pathlib
import re
import sys
import traceback
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPS_DIR = ROOT / "apps"
COMMUN_CONSTS = ROOT / "apps" / "comun" / "consts.py"

sys.path.insert(0, str(ROOT))
from apps.comun.consts import HistoriasUsuario
from tools.constants import (
    DESCRIPTION,
    ENTRY,
    FILE,
    HUS,
    ID,
    LINE,
    LINEO,
    META,
    NO_DESC,
    RAW,
    VIEW,
    VIEWS,
)


def normalize_hu_key(hu_str: str) -> str:
    if not hu_str:
        return hu_str
    base = hu_str.split(".")[-1]
    m = re.search(r"(\d+)", base)
    if m:
        num = int(m.group(1))
        return f"HU{num:03d}"
    return base


def extract_hus_from_meta(class_node: ast.ClassDef) -> List[Dict[str, Any]]:
    results = []
    for node in class_node.body:
        if isinstance(node, ast.ClassDef) and node.name == META:
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if getattr(target, ID, None) == HUS:
                            value = stmt.value
                            if isinstance(value, ast.List):
                                for elt in value.elts:
                                    raw = None
                                    lineno = getattr(elt, LINEO, getattr(stmt, LINEO, None))

                                    if isinstance(elt, ast.Attribute) and isinstance(elt.value, ast.Name):
                                        raw = f"{elt.value.id}.{elt.attr}"
                                    elif isinstance(elt, ast.Name):
                                        raw = elt.id
                                    elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        raw = elt.value

                                    if raw:
                                        results.append({RAW: raw, LINEO: lineno})
    return results


def scan_views(include_location: bool = False) -> Dict[str, List[Any]]:
    mapping: Dict[str, List[Any]] = {}

    for views_path in APPS_DIR.rglob("views.py"):
        try:
            text = views_path.read_text(encoding="utf-8")
        except Exception:
            traceback.print_exc()
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            traceback.print_exc()
            continue

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                hus = extract_hus_from_meta(node)
                if not hus:
                    continue

                app_name = views_path.parent.name
                view_fullname = f"{app_name}.views.{node.name}"

                for hu_info in hus:
                    raw = hu_info.get(RAW)
                    lineno = hu_info.get(LINEO)
                    key = normalize_hu_key(raw)

                    if include_location:
                        entry = {
                            VIEW: view_fullname,
                            FILE: str(views_path.relative_to(ROOT)),
                            LINE: lineno,
                        }
                    else:
                        entry = view_fullname

                    mapping.setdefault(key, []).append({RAW: raw, ENTRY: entry})

    final: Dict[str, List[Any]] = {}
    for hu, items in mapping.items():
        views_list = []
        constants = []
        for it in items:
            raw = it.get(RAW)
            entry = it.get(ENTRY)
            const = raw.split(".")[-1] if raw else raw
            if const and const not in constants:
                constants.append(const)
            views_list.append(entry)

        final[hu] = {"enum_constants": constants, VIEWS: views_list}

    return final


def extract_hu_descriptions(consts_path: pathlib.Path) -> Dict[str, str]:
    descriptions: Dict[str, str] = {}
    if not consts_path.exists():
        return descriptions

    text = consts_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "=" in line and "HU_" in line:
            parts = line.split("#", 1)
            left = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ""
            left_name = left.split("=")[0].strip()
            if left_name.startswith("HU_") or left_name.startswith("HU"):
                descriptions[left_name] = comment

    return descriptions


def generate_documentation(include_location: bool = False) -> Dict[str, Any]:
    scanned = scan_views(include_location=include_location)
    docs: Dict[str, Any] = {}

    for hu_id, info in scanned.items():
        views_list = []
        for entry in info.get(VIEWS, []):
            if include_location:
                views_list.append(entry)
            else:
                if isinstance(entry, dict):
                    views_list.append(entry.get(VIEW))
                else:
                    views_list.append(entry)

        try:
            hu_enum = HistoriasUsuario(hu_id)
            description = hu_enum.describe()
        except ValueError:
            description = NO_DESC

        docs[hu_id] = {VIEWS: views_list, DESCRIPTION: description}

    return docs


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generates JSON HU -> Views (static analysis)")
    parser.add_argument(
        "--output", "-o", help="Output JSON file (default: hu_documentation.json)", default="hu_documentation.json"
    )
    parser.add_argument(
        "--include-location", action="store_true", help="Include file and line where the HU was declared"
    )
    args = parser.parse_args()

    docs = generate_documentation(include_location=args.include_location)

    text = json.dumps(docs, indent=2, ensure_ascii=False)
    pathlib.Path(args.output).write_text(text, encoding="utf-8")
    print(f"JSON saved to {args.output}")


if __name__ == "__main__":
    main()
