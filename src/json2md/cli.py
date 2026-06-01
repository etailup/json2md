from __future__ import annotations

import argparse
import sys
from pathlib import Path

from json2md.converter import json_to_markdown, parse_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="json2md",
        description="Convert JSON into readable Markdown documentation.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="JSON file path. Reads stdin when omitted.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write Markdown to this file instead of stdout.",
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Optional document title for the Markdown output.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.input:
        raw = Path(args.input).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        parser.print_help()
        raise SystemExit(1)

    data = parse_json(raw)
    markdown = json_to_markdown(data, title=args.title)

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
