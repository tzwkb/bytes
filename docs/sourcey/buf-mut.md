---
title: Encode with BufMut
description: Write generic byte output while respecting capacity and initialization invariants.
---

# Encode with BufMut

`BufMut` is the cursor-based writing counterpart to [`Buf`](buf.md). It can
target a `BytesMut`, `Vec<u8>`, or a fixed mutable slice. Generic encoders
accept `&mut impl BufMut` and write fields with `put_slice` or numeric helpers.
The trait is `unsafe` to implement because its low-level cursor must never
expose uninitialized bytes as initialized data; application code normally uses
the safe provided methods instead.

```rust
use bytes::{BufMut, BytesMut};

fn put_record(dst: &mut impl BufMut, body: &[u8]) {
    dst.put_u8(body.len() as u8);
    dst.put_slice(body);
}

let mut out = BytesMut::new();
put_record(&mut out, b"ok");
assert_eq!(&out[..], b"\x02ok");
```

Growable destinations can allocate during writes; fixed slices cannot. Plan
capacity for the entire field before a `put_*` call when the destination may
not grow. See [`BytesMut`](bytes-mut.md) for reserving and explicit spare
capacity, and [`Adapters`](adapters.md) for the `std` writer bridge.

## `BufMut`

Usage: accept `&mut impl BufMut` for an encoder. It models writable bytes from
the current cursor to the end, potentially over non-contiguous storage. The
unsafe implementation contract requires `advance_mut` to expose only bytes
that have been initialized; users should rely on safe methods unless filling
raw memory is necessary. [View pinned source](https://github.com/tokio-rs/bytes/blob/d5c8ad3227afe459c09f1d0d85455abf00f0381a/src/buf/buf_mut.rs#L30)

## `BufMut::remaining_mut`

Usage: `buf.remaining_mut() -> usize`. It reports writable capacity from the
cursor and is at least the current mutable chunk length. It may under-report
actual possible space and allocation can still fail before that amount is
reached. Use it to protect fixed buffers, not as a promise that a growable
buffer will never allocate. [View pinned source](https://github.com/tokio-rs/bytes/blob/d5c8ad3227afe459c09f1d0d85455abf00f0381a/src/buf/buf_mut.rs#L64)

## `BufMut::put_slice`

Usage: `buf.put_slice(src)`. It copies all source bytes and advances the cursor
by `src.len()`, walking chunks if needed. It panics if the destination lacks
enough remaining capacity, so reserve or reject oversized fixed-frame input
before writing. [View pinned source](https://github.com/tokio-rs/bytes/blob/d5c8ad3227afe459c09f1d0d85455abf00f0381a/src/buf/buf_mut.rs#L246)

## `BufMut::put_u8`

Usage: `buf.put_u8(value)`. It writes one byte and advances the cursor once.
The method delegates to `put_slice`, so it panics if no writable capacity is
available. This is useful for tags and length prefixes after checking that the
protocol value fits in `u8`. [View pinned source](https://github.com/tokio-rs/bytes/blob/d5c8ad3227afe459c09f1d0d85455abf00f0381a/src/buf/buf_mut.rs#L330)

## `UninitSlice`

Usage: `bytes::buf::UninitSlice` is the wrapper returned by `chunk_mut` around
possibly uninitialized storage. Reading it or writing uninitialized bytes into
it is undefined behavior; write concrete byte values, then advance only that
initialized count. Its checked indexing still panics out of bounds. Prefer
safe `put_slice` for normal encoding. [View pinned source](https://github.com/tokio-rs/bytes/blob/d5c8ad3227afe459c09f1d0d85455abf00f0381a/src/buf/uninit_slice.rs#L22)
