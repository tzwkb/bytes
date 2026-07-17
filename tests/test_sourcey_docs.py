import json
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "sourcey"


class SourceyDocsTests(unittest.TestCase):
    def inventory(self):
        return json.loads((DOCS / "api-inventory.json").read_text(encoding="utf-8"))

    def test_inventory_has_at_least_twenty_public_apis(self):
        self.assertGreaterEqual(len(self.inventory()["apis"]), 20)

    def test_inventory_pins_upstream_metadata(self):
        inventory = self.inventory()
        self.assertEqual(inventory["repository"], "https://github.com/tokio-rs/bytes")
        self.assertEqual(inventory["commit"], "d5c8ad3227afe459c09f1d0d85455abf00f0381a")
        self.assertEqual(inventory["license"], "MIT")

    def test_every_mapping_matches_pinned_source_line(self):
        for item in self.inventory()["apis"]:
            path = ROOT / item["source_path"]
            self.assertTrue(path.is_file(), item["source_path"])
            lines = path.read_text(encoding="utf-8").splitlines()
            source_line = item["source_line"]
            context = f'{item["symbol"]}: {item["source_path"]}:{source_line}'
            self.assertGreaterEqual(source_line, 1, f"{context} is out of range")
            self.assertLessEqual(source_line, len(lines), f"{context} is out of range")
            line = lines[source_line - 1]
            self.assertIn(item["source_token"], line, item["symbol"])

    def test_out_of_range_mapping_has_symbol_and_path_context(self):
        item = {
            "symbol": "Bytes::past_end",
            "source_path": "src/bytes.rs",
            "source_line": 999999,
            "source_token": "pub fn past_end",
        }
        with patch.object(self, "inventory", return_value={"apis": [item]}):
            with self.assertRaisesRegex(AssertionError, r"Bytes::past_end.*src/bytes\.rs"):
                self.test_every_mapping_matches_pinned_source_line()

    def test_required_pages_exist_and_are_substantive(self):
        required = {
            "index.md", "installation.md", "bytes.md", "bytes-mut.md",
            "buf.md", "buf-mut.md", "adapters.md", "patterns.md",
        }
        for name in required:
            text = (DOCS / name).read_text(encoding="utf-8")
            self.assertGreaterEqual(len(text.split()), 180, name)

    def test_inventory_pages_resolve(self):
        for item in self.inventory()["apis"]:
            self.assertTrue((DOCS / item["page"]).is_file(), item["page"])


if __name__ == "__main__":
    unittest.main()
