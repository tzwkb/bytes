# Bytes Sourcey Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and submit a stranger-accessible Sourcey documentation site for `tokio-rs/bytes` that satisfies every Frantic bounty #46 criterion.

**Architecture:** Keep upstream Rust code unchanged and add a bounded documentation layer under `docs/sourcey/`. A JSON API inventory is validated against the pinned Rust source, Sourcey 3.6.5 builds static HTML, and Read the Docs publishes the fork. Immutable evidence and report URLs bind the live site to one delivery commit and a governed runx receipt.

**Tech Stack:** Rust 2021 source tree, Python 3 standard-library tests, Node.js 20, Sourcey 3.6.5, Read the Docs, runx CLI 0.6.6+, Frantic API.

## Global Constraints

- Upstream source remains pinned to `d5c8ad3227afe459c09f1d0d85455abf00f0381a`.
- The target is `https://github.com/tokio-rs/bytes`, version `1.12.1`, MIT licensed.
- Document at least 20 public APIs and at least six substantive pages.
- The site is supplemental task-oriented documentation; do not claim upstream adoption or ownership.
- Use a dedicated Read the Docs project backed by the public `tzwkb/bytes` fork.
- Use exact artifact names: `public_url`, `evidence_json`, `receipt_ref`, `report`.
- Inspect the current Frantic OpenAPI immediately before every write.
- Never expose Frantic tokens or wallet signing secrets.
- Count income only after settlement and confirmed wallet receipt.

---

### Task 1: Claim the funded slot and lock the documentation contract

**Files:**
- Create: `tests/test_sourcey_docs.py`
- Create: `docs/sourcey/api-inventory.json`

**Interfaces:**
- Consumes: Frantic bounty #46 and pinned Rust tree.
- Produces: active claim ID/deadline stored privately and a test-enforced documentation contract.

- [ ] **Step 1: Recheck and claim #46**

Run:

```bash
cd /Users/spellbook/.codex/skills/frantic-earner
python3 scripts/frantic_read.py bounty 46
curl -fsS https://gofrantic.com/openapi.json | jq '.paths["/v1/claims"]'
```

Expected: bounty is funded with one available slot and the live request schema is visible. Submit the claim with a short Python process that reads `~/.config/frantic/agent.json` in memory, writes the response to `~/.config/frantic/claim-46.json` with mode `600`, and prints only claim ID and deadline.

- [ ] **Step 2: Write the failing contract tests**

Create `tests/test_sourcey_docs.py` with:

```python
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
```

- [ ] **Step 3: Run tests and verify the intended failure**

Run: `python3 -m unittest tests.test_sourcey_docs -v`

Expected: failure because `docs/sourcey/api-inventory.json` and required pages do not exist.

- [ ] **Step 4: Add the initial API inventory**

Create `docs/sourcey/api-inventory.json` with these 31 pinned mappings:

```json
{
  "ecosystem": "Rust",
  "repository": "https://github.com/tokio-rs/bytes",
  "commit": "d5c8ad3227afe459c09f1d0d85455abf00f0381a",
  "license": "MIT",
  "apis": [
    {"symbol":"Bytes::new","source_path":"src/bytes.rs","source_line":151,"source_token":"pub fn new()","category":"immutable-buffer","page":"bytes.md"},
    {"symbol":"Bytes::from_static","source_path":"src/bytes.rs","source_line":182,"source_token":"pub fn from_static","category":"immutable-buffer","page":"bytes.md"},
    {"symbol":"Bytes::copy_from_slice","source_path":"src/bytes.rs","source_line":347,"source_token":"pub fn copy_from_slice","category":"immutable-buffer","page":"bytes.md"},
    {"symbol":"Bytes::slice","source_path":"src/bytes.rs","source_line":373,"source_token":"pub fn slice","category":"immutable-buffer","page":"bytes.md"},
    {"symbol":"Bytes::split_off","source_path":"src/bytes.rs","source_line":472,"source_token":"pub fn split_off","category":"immutable-buffer","page":"bytes.md"},
    {"symbol":"Bytes::split_to","source_path":"src/bytes.rs","source_line":523,"source_token":"pub fn split_to","category":"immutable-buffer","page":"bytes.md"},
    {"symbol":"Bytes::try_into_mut","source_path":"src/bytes.rs","source_line":620,"source_token":"pub fn try_into_mut","category":"conversion","page":"patterns.md"},
    {"symbol":"BytesMut::with_capacity","source_path":"src/bytes_mut.rs","source_line":161,"source_token":"pub fn with_capacity","category":"mutable-buffer","page":"bytes-mut.md"},
    {"symbol":"BytesMut::freeze","source_path":"src/bytes_mut.rs","source_line":259,"source_token":"pub fn freeze","category":"conversion","page":"patterns.md"},
    {"symbol":"BytesMut::reserve","source_path":"src/bytes_mut.rs","source_line":615,"source_token":"pub fn reserve","category":"mutable-buffer","page":"bytes-mut.md"},
    {"symbol":"BytesMut::extend_from_slice","source_path":"src/bytes_mut.rs","source_line":892,"source_token":"pub fn extend_from_slice","category":"mutable-buffer","page":"bytes-mut.md"},
    {"symbol":"BytesMut::unsplit","source_path":"src/bytes_mut.rs","source_line":969,"source_token":"pub fn unsplit","category":"mutable-buffer","page":"bytes-mut.md"},
    {"symbol":"BytesMut::spare_capacity_mut","source_path":"src/bytes_mut.rs","source_line":1211,"source_token":"pub fn spare_capacity_mut","category":"mutable-buffer","page":"bytes-mut.md"},
    {"symbol":"Buf","source_path":"src/buf/buf_impl.rs","source_line":122,"source_token":"pub trait Buf","category":"read-trait","page":"buf.md"},
    {"symbol":"Buf::remaining","source_path":"src/buf/buf_impl.rs","source_line":148,"source_token":"fn remaining","category":"read-trait","page":"buf.md"},
    {"symbol":"Buf::chunk","source_path":"src/buf/buf_impl.rs","source_line":181,"source_token":"fn chunk","category":"read-trait","page":"buf.md"},
    {"symbol":"Buf::advance","source_path":"src/buf/buf_impl.rs","source_line":255,"source_token":"fn advance","category":"read-trait","page":"buf.md"},
    {"symbol":"Buf::get_u8","source_path":"src/buf/buf_impl.rs","source_line":320,"source_token":"fn get_u8","category":"read-trait","page":"buf.md"},
    {"symbol":"Buf::copy_to_bytes","source_path":"src/buf/buf_impl.rs","source_line":2363,"source_token":"fn copy_to_bytes","category":"read-trait","page":"buf.md"},
    {"symbol":"Buf::take","source_path":"src/buf/buf_impl.rs","source_line":2399,"source_token":"fn take","category":"adapter","page":"adapters.md"},
    {"symbol":"Buf::reader","source_path":"src/buf/buf_impl.rs","source_line":2453,"source_token":"fn reader","category":"adapter","page":"adapters.md"},
    {"symbol":"BufMut","source_path":"src/buf/buf_mut.rs","source_line":30,"source_token":"pub unsafe trait BufMut","category":"write-trait","page":"buf-mut.md"},
    {"symbol":"BufMut::remaining_mut","source_path":"src/buf/buf_mut.rs","source_line":64,"source_token":"fn remaining_mut","category":"write-trait","page":"buf-mut.md"},
    {"symbol":"BufMut::put_slice","source_path":"src/buf/buf_mut.rs","source_line":246,"source_token":"fn put_slice","category":"write-trait","page":"buf-mut.md"},
    {"symbol":"BufMut::put_u8","source_path":"src/buf/buf_mut.rs","source_line":330,"source_token":"fn put_u8","category":"write-trait","page":"buf-mut.md"},
    {"symbol":"BufMut::writer","source_path":"src/buf/buf_mut.rs","source_line":1317,"source_token":"fn writer","category":"adapter","page":"adapters.md"},
    {"symbol":"Chain","source_path":"src/buf/chain.rs","source_line":30,"source_token":"pub struct Chain","category":"adapter","page":"adapters.md"},
    {"symbol":"Take","source_path":"src/buf/take.rs","source_line":13,"source_token":"pub struct Take","category":"adapter","page":"adapters.md"},
    {"symbol":"Reader","source_path":"src/buf/reader.rs","source_line":11,"source_token":"pub struct Reader","category":"adapter","page":"adapters.md"},
    {"symbol":"Writer","source_path":"src/buf/writer.rs","source_line":11,"source_token":"pub struct Writer","category":"adapter","page":"adapters.md"},
    {"symbol":"UninitSlice","source_path":"src/buf/uninit_slice.rs","source_line":22,"source_token":"pub struct UninitSlice","category":"write-trait","page":"buf-mut.md"}
  ]
}
```

- [ ] **Step 5: Commit the claim contract**

```bash
git add tests/test_sourcey_docs.py docs/sourcey/api-inventory.json
git commit -m "test: define Sourcey docs contract"
```

### Task 2: Write task-oriented Rust documentation

**Files:**
- Create: `docs/sourcey/index.md`
- Create: `docs/sourcey/installation.md`
- Create: `docs/sourcey/bytes.md`
- Create: `docs/sourcey/bytes-mut.md`
- Create: `docs/sourcey/buf.md`
- Create: `docs/sourcey/buf-mut.md`
- Create: `docs/sourcey/adapters.md`
- Create: `docs/sourcey/patterns.md`

**Interfaces:**
- Consumes: `docs/sourcey/api-inventory.json`.
- Produces: eight substantive Sourcey Markdown pages with cross-links and runnable Rust examples.

- [ ] **Step 1: Draft the eight pages**

Each file must include Sourcey frontmatter with `title` and `description`, one H1, task-oriented prose, at least one Rust example where appropriate, and links to related pages. Keep examples compatible with `bytes = "1"`; identify `std`, `serde`, and `extra-platforms` feature requirements explicitly.

- [ ] **Step 2: Add source mapping blocks**

For every inventory entry, add a visible API section to its destination page with the exact symbol, signature or usage, behavior, edge conditions, and a source link of this form:

```markdown
[View pinned source](https://github.com/tokio-rs/bytes/blob/d5c8ad3227afe459c09f1d0d85455abf00f0381a/src/bytes.rs#L151)
```

- [ ] **Step 3: Run contract tests**

Run: `python3 -m unittest tests.test_sourcey_docs -v`

Expected: all inventory, source-line, page-existence, and substantive-content tests pass.

- [ ] **Step 4: Run Rust tests**

Run: `cargo test --all-features`

Expected: upstream test suite passes without modifying Rust implementation files.

- [ ] **Step 5: Commit the documentation content**

```bash
git add docs/sourcey
git commit -m "docs: add task-oriented bytes guides"
```

### Task 3: Configure and verify deterministic Sourcey builds

**Files:**
- Create: `docs/sourcey/sourcey.config.ts`
- Create: `package.json`
- Create: `package-lock.json`
- Create: `.readthedocs.yaml`
- Modify: `.gitignore`
- Modify: `tests/test_sourcey_docs.py`

**Interfaces:**
- Consumes: eight Markdown pages and API inventory.
- Produces: reproducible `npm run docs:build` output accepted by Read the Docs.

- [ ] **Step 1: Extend tests for build configuration**

Add tests that assert `sourcey.config.ts`, `.readthedocs.yaml`, and `package.json` exist; package-lock resolves Sourcey exactly to `3.6.5`; navigation references all eight pages; and the Read the Docs command writes to `$READTHEDOCS_OUTPUT/html`.

- [ ] **Step 2: Verify the new tests fail**

Run: `python3 -m unittest tests.test_sourcey_docs -v`

Expected: configuration tests fail because the files are absent.

- [ ] **Step 3: Add Sourcey configuration**

Create `docs/sourcey/sourcey.config.ts`:

```typescript
import { defineConfig, markdown } from "sourcey";

const canonicalUrl = new URL(
  process.env.READTHEDOCS_CANONICAL_URL ??
    "https://bytes-field-guide.readthedocs.io/en/latest/",
);

export default defineConfig({
  name: "Bytes Field Guide",
  siteUrl: canonicalUrl.origin,
  baseUrl: canonicalUrl.pathname,
  repo: "https://github.com/tzwkb/bytes",
  editBranch: "main",
  editBasePath: "docs/sourcey",
  navigation: {
    tabs: [
      {
        tab: "Guide",
        slug: "",
        source: markdown({
          groups: [
            { group: "Start", pages: ["index", "installation"] },
            { group: "Buffer Types", pages: ["bytes", "bytes-mut"] },
            { group: "Traits", pages: ["buf", "buf-mut"] },
            { group: "Workflows", pages: ["adapters", "patterns"] },
          ],
        }),
      },
    ],
  },
});
```

- [ ] **Step 4: Add pinned Node and Read the Docs configuration**

Create `package.json`:

```json
{
  "name": "bytes-sourcey-docs",
  "private": true,
  "scripts": {
    "docs:build": "cd docs/sourcey && sourcey build"
  },
  "devDependencies": {
    "sourcey": "3.6.5"
  }
}
```

Run `npm install --package-lock-only`, then create `.readthedocs.yaml`:

```yaml
version: 2

build:
  os: ubuntu-24.04
  tools:
    nodejs: "20"
  jobs:
    install:
      - npm ci
    build:
      html:
        - npm run docs:build -- --output "$READTHEDOCS_OUTPUT/html" --quiet
```

Add `.sourcey/`, `node_modules/`, and local generated output to `.gitignore`.

- [ ] **Step 5: Build and validate generated output**

Run:

```bash
npm ci
out="$(mktemp -d)"
npm run docs:build -- --output "$out" --quiet
test -f "$out/index.html"
test -f "$out/search-index.json"
test -f "$out/sitemap.xml"
test -f "$out/llms.txt"
test -f "$out/llms-full.txt"
```

Extend `tests/test_sourcey_docs.py` to parse generated links and fail on missing internal targets. Run the full test again and expect PASS.

- [ ] **Step 6: Commit the build system**

```bash
git add .gitignore .readthedocs.yaml package.json package-lock.json docs/sourcey/sourcey.config.ts tests/test_sourcey_docs.py
git commit -m "build: configure Sourcey and Read the Docs"
```

### Task 4: Publish the fork and live Read the Docs site

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: deterministic local build.
- Produces: public fork commit and stranger-accessible HTTPS site.

- [ ] **Step 1: Create or reuse the public fork**

Use GitHub CLI to create `tzwkb/bytes` only if it does not exist. Point a writable remote at the fork, push `codex/sourcey-docs`, merge it into the fork's `main` without altering upstream history, and record the exact delivery commit.

- [ ] **Step 2: Add the public documentation link**

Add a short `Community task-oriented guide` link to `README.md`, run `git diff --check`, commit, and push the exact state that will be deployed.

- [ ] **Step 3: Import the fork into Read the Docs**

Create the dedicated project slug `bytes-field-guide` from `https://github.com/tzwkb/bytes.git`, default branch `main`, and trigger the build. Preserve the logged-in Chrome tabs; ask the user only for CAPTCHA, OTP, or authentication if the session expires.

- [ ] **Step 4: Verify the public site as a stranger**

Run HTTP checks against `https://bytes-field-guide.readthedocs.io/en/latest/` for the landing page, all eight content pages, `search-index.json`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, and representative assets. Parse every internal link and require HTTP 200. Spot-check at least three rendered source mappings against the pinned repository.

- [ ] **Step 5: Commit deployment metadata**

Record the Read the Docs project, build ID, public URL, commit, page count, mapping count, and public check results in the evidence files created in Task 5.

### Task 5: Build immutable evidence and governed receipt

**Files:**
- Create: `docs/bounty/frantic-46/evidence.json`
- Create: `docs/bounty/frantic-46/report.md`
- Create: `docs/bounty/frantic-46/receipts/<sha256>.json`
- Modify: `tests/test_sourcey_docs.py`

**Interfaces:**
- Consumes: live site, deployment commit, validator results, runx 0.6.6+.
- Produces: immutable public evidence URLs and `runx:receipt:sha256:<digest>`.

- [ ] **Step 1: Add evidence contract tests**

Test that `evidence.json` is valid JSON; has a nontrivial `artifact_summary`; contains at least six observations; records exact ecosystem, repository, commit, license, adapter, build command/config, page list, gaps, public checks, and exact `runx --version`; and that `report.md` has at least six bullets and no placeholder text.

- [ ] **Step 2: Write evidence and report**

Use only observed facts. Explicitly state that the site is a supplemental community guide hosted from the public fork and is not represented as official upstream adoption. Include the exact generated page list, at least three source-map spot checks, all validator commands/results, Read the Docs build ID, and any remaining gaps.

- [ ] **Step 3: Generate the governed runx receipt**

Run `runx --version` and require `runx-cli 0.6.6` or newer. Execute the governed validation over the committed artifact set, save the public receipt JSON under `docs/bounty/frantic-46/receipts/`, and verify its digest recomputes to the receipt reference.

- [ ] **Step 4: Run complete local verification**

```bash
python3 -m unittest tests.test_sourcey_docs -v
cargo test --all-features
npm ci
out="$(mktemp -d)"
npm run docs:build -- --output "$out" --quiet
jq empty docs/sourcey/api-inventory.json docs/bounty/frantic-46/evidence.json docs/bounty/frantic-46/receipts/*.json
git diff --check
```

Expected: every command passes and the generated site contains all required assets and links.

- [ ] **Step 5: Commit and push immutable evidence**

```bash
git add docs/bounty/frantic-46 tests/test_sourcey_docs.py
git commit -m "docs: add Frantic 46 delivery evidence"
git push
```

Verify the raw GitHub URLs for `evidence.json`, `report.md`, and the receipt return HTTP 200 at this exact commit.

### Task 6: Preflight, deliver once, and verify payment

**Files:**
- Store privately: `~/.config/frantic/preflight-46.json`
- Store privately: `~/.config/frantic/delivery-46.json`
- Modify after settlement: `/Users/spellbook/Documents/moneymaking/deliverables/earnings-ledger.md`

**Interfaces:**
- Consumes: four public bounty artifacts and active claim.
- Produces: accepted Frantic delivery and, after settlement, authoritative earnings evidence.

- [ ] **Step 1: Inspect the live write schemas**

```bash
curl -fsS https://gofrantic.com/openapi.json | jq '.paths["/v1/deliveries/preflight"], .paths["/v1/deliveries"]'
```

Construct request bodies only from the current schemas. Read credentials from `~/.config/frantic/agent.json` in process memory and never print them.

- [ ] **Step 2: Run preflight**

Bind the exact names:

```text
public_url=https://bytes-field-guide.readthedocs.io/en/latest/
evidence_json=https://raw.githubusercontent.com/tzwkb/bytes/<commit>/docs/bounty/frantic-46/evidence.json
receipt_ref=runx:receipt:sha256:<digest>
report=https://raw.githubusercontent.com/tzwkb/bytes/<commit>/docs/bounty/frantic-46/report.md
```

Expected: all artifacts bound, no blocking errors, and no unresolved warnings. Save the sanitized response privately with mode `600`.

- [ ] **Step 3: Deliver exactly once**

Submit the same bindings to the live delivery endpoint. Store the private response with mode `600` and print only delivery ID, receipt reference, and stage. Do not resubmit while review is pending.

- [ ] **Step 4: Monitor review and address evidence-based revisions**

Run `python3 scripts/frantic_read.py status`. If revision is requested, change only what the review evidence requires, revalidate, and submit one revision. Keep posted, pending, accepted/owed, and received amounts separate.

- [ ] **Step 5: Verify settlement before accounting**

After Frantic reports `paid`, verify the Base transaction or wallet balance delta for `0x748eE02828418f7225FAEb230cDd9cEAa308C111`. Only then add 16 USDC to `deliverables/earnings-ledger.md` and recalculate progress toward 50 USD.
