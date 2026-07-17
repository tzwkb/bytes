# Bytes Field Guide Sourcey documentation report

## Delivery summary

- Published an eight-page Sourcey 3.6.5 site for `tokio-rs/bytes`, a maintained MIT-licensed Rust library pinned at upstream commit `d5c8ad3227afe459c09f1d0d85455abf00f0381a` and package version 1.12.1.
- Documented 31 public APIs and types from nine Rust source files, above the 15-entry acceptance threshold; every mapping records an exact source path, line, token, category, and guide page.
- Added task-oriented pages for installation, `Bytes`, `BytesMut`, `Buf`, `BufMut`, adapters, and framing patterns, with generated navigation rather than a landing-page-only artifact.
- Published the site at `bytes-field-guide.readthedocs.io` from `tzwkb/bytes` branch `main` using the committed `.readthedocs.yaml` and exact Sourcey dependency lock.
- Verified Read the Docs build `#33628289` succeeded at deployment commit `c6bc06d8ad9ad1618d023bd2aad3b4c954c20952`.
- Rechecked the public surface without authentication: all eight pages plus Sourcey CSS, JavaScript, search index, sitemap, `llms.txt`, and `llms-full.txt` returned HTTP 200.
- Ran 13 focused documentation contract tests covering source pinning, all 31 line mappings, page substance, navigation, dependency pinning, Read the Docs output, generated assets, internal links, same-page fragments, and cross-page fragments; all passed.
- Sealed the governed Sourcey run with `runx-cli 0.7.2` as `runx:receipt:sha256:967f8492ab6f8cfc206d5ae074973bc7149b72c1c3ba12835367108f675ed28d`.
- Verified the public receipt tree in local-development signature mode: 12 receipts, no missing parent, no unreadable files, and no findings.
- Kept generated HTML outside version control; the repository contains the authored pages, Sourcey config, exact lockfile, deployment config, tests, evidence, report, and recomputable receipt tree.

## User value

- The ownership boundary is explicit: build with `BytesMut`, publish with `freeze`, and recover mutability only when `try_into_mut` can prove uniqueness.
- Cursor examples check `remaining()` before fixed-width reads and explain why `chunk()` cannot be assumed to contain an entire logical message.
- Write examples distinguish growable `BytesMut` destinations from fixed-capacity `BufMut` implementations and show where `reserve` is required.
- Adapter guidance separates bytes-native code from APIs that specifically require `std::io::Read` or `std::io::Write`.
- Every API claim links to immutable upstream source, so readers and reviewers can spot-check the documentation without trusting prose alone.
- Generated search, sitemap, Open Graph assets, and LLM-oriented text make the guide useful beyond direct page navigation.

## Maintainer-facing gaps

- This is a community supplemental field guide maintained in `tzwkb/bytes`; it is not an upstream `tokio-rs/bytes` publication or endorsement.
- The inventory is intentionally pinned to bytes 1.12.1. An upstream release can move source lines or change safety contracts, so future updates must rerun the mapping tests before deployment.
- Manual Read the Docs setup does not add an upstream repository webhook. Future documentation commits require a Read the Docs rebuild unless GitHub integration permissions are expanded.
- The guide focuses on decision points and examples rather than replacing the crate's complete rustdoc reference.
- Advanced no-std and portable-atomic behavior is introduced during installation but is not expanded into a platform compatibility matrix.
- Performance claims are kept qualitative; no benchmark suite is included because allocation and copy costs depend on workload and target platform.

## Why this is a credible home

The live site is a dedicated `bytes-field-guide.readthedocs.io` project built directly from the public `tzwkb/bytes` documentation fork and linked from that fork's README. The fork preserves upstream history, pins the source commit, keeps deployment configuration next to the docs, and states the community relationship without implying upstream ownership. The home is project-specific, stranger-reachable, reproducible from committed source, and backed by a public receipt tree; it is not a personal-handle Pages site, temporary preview, or detached demo host.
