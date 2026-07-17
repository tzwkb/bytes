import json
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "sourcey"
PAGES = (
    "index",
    "installation",
    "bytes",
    "bytes-mut",
    "buf",
    "buf-mut",
    "adapters",
    "patterns",
)


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for name in ("href", "src"):
            if attributes.get(name):
                self.urls.append(attributes[name])


def is_local_url(url):
    parsed = urlsplit(url)
    return not parsed.scheme and not parsed.netloc and parsed.path


def output_target(output, page, url):
    path = unquote(urlsplit(url).path)
    if path.startswith("/en/latest/"):
        path = path.removeprefix("/en/latest/")
    elif path.startswith("/"):
        path = path.lstrip("/")
    else:
        path = (page.parent / path).relative_to(output).as_posix()

    target = output / path
    return target / "index.html" if target.is_dir() else target


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

    def test_sourcey_build_configuration_exists(self):
        self.assertTrue((DOCS / "sourcey.config.ts").is_file())
        self.assertTrue((ROOT / "package.json").is_file())
        self.assertTrue((ROOT / ".readthedocs.yaml").is_file())

    def test_sourcey_navigation_references_every_page(self):
        self.assertTrue((DOCS / "sourcey.config.ts").is_file())
        config = (DOCS / "sourcey.config.ts").read_text(encoding="utf-8")
        for page in PAGES:
            self.assertIn(f'"{page}"', config)

    def test_package_lock_pins_sourcey_exactly(self):
        self.assertTrue((ROOT / "package.json").is_file())
        self.assertTrue((ROOT / "package-lock.json").is_file())
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
        self.assertEqual(package["devDependencies"]["sourcey"], "3.6.5")
        self.assertEqual(lock["packages"]["node_modules/sourcey"]["version"], "3.6.5")

    def test_readthedocs_writes_html_to_rtd_output(self):
        self.assertTrue((ROOT / ".readthedocs.yaml").is_file())
        config = (ROOT / ".readthedocs.yaml").read_text(encoding="utf-8")
        self.assertIn('npm run docs:build -- --output "$READTHEDOCS_OUTPUT/html" --quiet', config)

    @unittest.skipUnless((ROOT / "package.json").is_file(), "Sourcey build configuration has not been created")
    def test_generated_site_assets_and_internal_links_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            subprocess.run(
                ["npm", "run", "docs:build", "--", "--output", str(output), "--quiet"],
                cwd=ROOT,
                check=True,
            )

            for name in ("index.html", "search-index.json", "sitemap.xml", "llms.txt", "llms-full.txt"):
                self.assertTrue((output / name).is_file(), name)

            missing = []
            for page in output.rglob("*.html"):
                parser = LinkCollector()
                parser.feed(page.read_text(encoding="utf-8"))
                for url in parser.urls:
                    if is_local_url(url):
                        target = output_target(output, page, url)
                        if not target.is_file():
                            missing.append(f"{page.relative_to(output)} -> {url}")
            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
