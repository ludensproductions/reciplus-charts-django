"""Warn when Django views are missing Meta.HUs.

This script is intended for prek and only warns (exit code 0).
It inspects the provided filenames, so it only checks staged files.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _has_hus_assignment(meta_node: ast.ClassDef) -> bool:
    """Return True if Meta contains an assignment to HUs.

    Args:
        meta_node: The Meta class node to inspect.

    Returns:
        True when Meta defines HUs.
    """
    for node in meta_node.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "HUs":
                    return True
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "HUs":
                return True
    return False


def _find_missing_hus(file_path: Path) -> list[tuple[int, str]]:
    """Find view classes that are missing Meta.HUs.

    Args:
        file_path: Path to a Python module.

    Returns:
        A list of tuples with (line_number, class_name).
    """
    try:
        source = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"WARNING: Could not read {file_path}: {exc}")
        return []

    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as exc:
        line_no = exc.lineno or 1
        print(f"WARNING: {file_path}:{line_no} has syntax errors; skipping Meta.HUs check.")
        return []

    missing: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        if not node.name.endswith("View"):
            continue

        meta_node = next(
            (child for child in node.body if isinstance(child, ast.ClassDef) and child.name == "Meta"),
            None,
        )
        if meta_node is None or not _has_hus_assignment(meta_node):
            missing.append((node.lineno, node.name))

    return missing


def main() -> int:
    """Entry point for the prek hook.

    Returns:
        Always 0 to avoid blocking commits.
    """
    file_args = [Path(arg) for arg in sys.argv[1:]]
    if not file_args:
        return 0

    for file_path in file_args:
        if file_path.suffix != ".py":
            continue
        missing = _find_missing_hus(file_path)
        for line_no, class_name in missing:
            print(f"WARNING: {file_path}:{line_no} class `{class_name}` is missing Meta.HUs.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
