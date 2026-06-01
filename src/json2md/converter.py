from __future__ import annotations

import json
from typing import Any


def json_to_markdown(data: Any, *, title: str | None = None, depth: int = 0) -> str:
    lines: list[str] = []
    if title and depth == 0:
        lines.append(f"# {title}\n")

    if isinstance(data, list):
        if not data:
            lines.append("_Empty list_\n")
        elif all(isinstance(item, dict) for item in data):
            lines.append(_array_of_objects_to_table(data))
        else:
            for index, item in enumerate(data, start=1):
                lines.append(f"## Item {index}\n")
                lines.append(json_to_markdown(item, depth=depth + 1))
    elif isinstance(data, dict):
        if not data:
            lines.append("_Empty object_\n")
        else:
            scalar_rows: list[tuple[str, str]] = []
            nested: list[tuple[str, Any]] = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    nested.append((key, value))
                else:
                    scalar_rows.append((key, _format_scalar(value)))

            if scalar_rows:
                lines.append("| Key | Value |")
                lines.append("| --- | --- |")
                for key, value in scalar_rows:
                    lines.append(f"| {_escape_cell(key)} | {_escape_cell(value)} |")
                lines.append("")

            for key, value in nested:
                heading = "#" * min(depth + 2, 6)
                lines.append(f"{heading} {key}\n")
                lines.append(json_to_markdown(value, depth=depth + 1))
    else:
        lines.append(f"{_format_scalar(data)}\n")

    return "\n".join(lines).rstrip() + "\n"


def _array_of_objects_to_table(rows: list[dict[str, Any]]) -> str:
    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                keys.append(key)

    lines = [
        "| " + " | ".join(_escape_cell(key) for key in keys) + " |",
        "| " + " | ".join("---" for _ in keys) + " |",
    ]
    for row in rows:
        cells = [_escape_cell(_format_scalar(row.get(key))) for key in keys]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def _format_scalar(value: Any) -> str:
    if value is None:
        return "`null`"
    if isinstance(value, bool):
        return "`true`" if value else "`false`"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if "\n" in value:
            return value
        return value
    return json.dumps(value, ensure_ascii=False)


def _escape_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def parse_json(text: str) -> Any:
    return json.loads(text)
