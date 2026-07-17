import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "sourcey"


class SourceyDocsTests(unittest.TestCase):
    def inventory(self):
        return json.loads((DOCS / "api-inventory.json").read_text(encoding="utf-8"))

    def test_inventory_has_at_least_twenty_public_apis(self):
        self.assertGreaterEqual(len(self.inventory()["apis"]), 20)

    def test_every_mapping_matches_pinned_source_line(self):
        for item in self.inventory()["apis"]:
            path = ROOT / item["source_path"]
            self.assertTrue(path.is_file(), item["source_path"])
            line = path.read_text(encoding="utf-8").splitlines()[item["source_line"] - 1]
            self.assertIn(item["source_token"], line, item["symbol"])

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
