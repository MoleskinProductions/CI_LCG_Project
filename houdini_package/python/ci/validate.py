from typing import Any, Dict

from jsonschema import Draft202012Validator


def _error_path(error) -> str:
    path = "$"
    for p in error.absolute_path:
        path += f"[{p!r}]"
    return path


def validate_json(instance: Dict[str, Any], schema: Dict[str, Any], label: str = "document") -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errors:
        first = errors[0]
        raise ValueError(f"{label} validation failed at {_error_path(first)}: {first.message}")
