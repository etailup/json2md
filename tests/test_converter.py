from __future__ import annotations

import json
import unittest

from json2md.converter import json_to_markdown, parse_json


class JsonToMarkdownTests(unittest.TestCase):
    def test_scalar_object(self) -> None:
        data = {"name": "json2md", "version": "0.1.0"}
        output = json_to_markdown(data, title="Package")
        self.assertIn("# Package", output)
        self.assertIn("| name | json2md |", output)
        self.assertIn("| version | 0.1.0 |", output)

    def test_array_of_objects_becomes_table(self) -> None:
        data = [{"id": 1, "name": "Alex"}, {"id": 2, "name": "Sam"}]
        output = json_to_markdown(data)
        self.assertIn("| id | name |", output)
        self.assertIn("| 1 | Alex |", output)
        self.assertIn("| 2 | Sam |", output)

    def test_nested_object(self) -> None:
        data = {"meta": {"env": "prod", "region": "eu-west"}}
        output = json_to_markdown(data)
        self.assertIn("## meta", output)
        self.assertIn("| env | prod |", output)

    def test_parse_json(self) -> None:
        self.assertEqual(parse_json('{"ok": true}'), {"ok": True})


if __name__ == "__main__":
    unittest.main()
