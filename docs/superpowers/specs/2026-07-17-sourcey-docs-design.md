# Sourcey Documentation Design

## Goal

Publish a durable, stranger-accessible Sourcey documentation site for the
`tokio-rs/bytes` Rust crate that satisfies Frantic bounty #46 and adds useful,
task-oriented guidance alongside the project's existing rustdoc.

## Scope

- Pin all generated documentation evidence to upstream commit
  `d5c8ad3227afe459c09f1d0d85455abf00f0381a`.
- Cover installation and feature selection, `Bytes`, `BytesMut`, `Buf`,
  `BufMut`, adapters, conversions, and common buffer workflows.
- Source-map at least 20 public APIs to their defining Rust files and lines.
- Publish through a dedicated Read the Docs project backed by the public fork.
- Produce the four exact bounty artifacts: `public_url`, `evidence_json`,
  `receipt_ref`, and `report`.

The site supplements rather than replaces docs.rs. It focuses on navigation,
cross-type workflows, and copyable examples that are harder to discover from
generated rustdoc alone.

## Architecture

The public fork contains a bounded documentation layer under `docs/sourcey/`,
a deterministic generator configuration, and validation tests. Sourcey reads
curated Markdown plus source metadata derived from the pinned Rust tree and
emits static HTML with generated navigation, search, sitemap, and LLM indexes.

Read the Docs builds the static site from the fork's default branch. The
published URL is the mutable public artifact; evidence and report URLs use the
immutable delivery commit. A governed runx invocation binds the validated
artifact set to a recomputable receipt.

## Components

1. **Source content**: six to eight substantive pages covering setup,
   immutable and mutable buffers, read/write traits, adapters, conversions,
   feature flags, and troubleshooting.
2. **API inventory**: a machine-readable manifest containing symbol, source
   path, source line, category, and destination page for at least 20 APIs.
3. **Sourcey configuration**: deterministic inputs, navigation order, site
   metadata, and output directory compatible with Read the Docs.
4. **Validation**: tests for API count, source-path existence, line mapping,
   required pages, generated navigation, internal links, and expected assets.
5. **Delivery evidence**: JSON observations and a Markdown report recording
   ecosystem, repository, pinned commit, MIT license, adapter/configuration,
   commands, page list, public checks, and known gaps.

## Data Flow

1. The API inventory references symbols in the pinned upstream source tree.
2. Validation checks every source mapping before generation.
3. Sourcey converts curated content and mappings into a static site.
4. Read the Docs builds and serves the generated site over HTTPS.
5. Stranger checks verify representative pages, assets, internal links, and
   source-mapped API entries.
6. Final evidence is committed, exposed through immutable raw GitHub URLs,
   validated with runx CLI 0.6.6 or newer, preflighted, and delivered once.

## Failure Handling

- A missing symbol, stale line mapping, broken internal link, or incomplete
  page fails local validation and blocks deployment.
- A Read the Docs build failure is corrected and rebuilt before evidence is
  finalized; preview URLs never qualify as `public_url`.
- Evidence records limitations honestly, including that the site is a
  supplemental community documentation surface rather than an upstream-owned
  replacement for docs.rs.
- A failed Frantic preflight blocks delivery. After a valid delivery, status is
  polled without duplicate submissions unless a revision is requested.

## Verification

- Run the repository's existing Rust tests where the local toolchain permits.
- Run focused documentation validators and Sourcey generation from a clean
  output directory.
- Require at least 20 valid source mappings and at least six generated content
  pages.
- Check generated HTML, navigation, search index, sitemap, `llms.txt`, and
  internal links.
- Verify the public site from outside the authenticated browser with HTTP 200
  checks and spot-check at least three source observations.
- Record the exact `runx --version` output; it must be `runx-cli 0.6.6` or
  newer.

## Acceptance Boundary

The work is ready to submit only when all four named artifacts are public, the
live site is stranger-accessible, every required observation is present, local
and public validators pass, and Frantic preflight reports no blocking errors.
Payment is counted toward the 50 USD goal only after Frantic settlement and a
confirmed wallet transaction or balance increase.
