# NUT-16 test vectors

The [machine-readable vectors](16-vectors.json) cover the binary fountain format and its Base45 QR mapping defined in [NUT-16](../16.md). Hex strings encode bytes; `qr_text` contains the exact scanner text, including any spaces. The synthetic token is not spendable.

## Frame and transfer vectors

- `transfers`: encode `message_hex` using the stated `fragment_size` and compare each listed sequence's selected `indexes`, `data_hex`, `frame_hex`, and `qr_text`. Reconstruct the message using systematic frames and, separately, only `mixed_only_recovery_sequences`. Reordering and identical duplicates do not change the result. Only entries with `scope: "token"` contain valid token structures; `token_text` is their original text serialization.
- `selection_vectors`: reproduce the selected indices independently of message bytes, including the all-zero-selector fallback and unsigned sequence boundaries.
- `valid_frames`: validate each frame and recompute its payload from the message pattern given in `note`. The nonuniform pattern exercises payload XOR across distinct fragments at the fragment-count and message-length limits. These are individual framing and Base45 codec cases; they do not imply complete reconstruction or that the text fits a physical QR symbol.
- `invalid_frames`: `frame_hex` and `qr_text` represent the same invalid input. `reject_at` identifies the first failing binary layer: `frame`, reconstructed `message`, or Cashu `token`. Oversized QR text may be rejected before reaching its binary layer. A valid frame checksum alone does not establish successful reconstruction or token validity.

## Base45 and QR mapping

- `base45_vectors`: compare encoding and decoding byte-for-byte against RFC 9285 examples and binary edge cases. The empty string is valid Base45 but is not a valid fountain frame.
- `invalid_qr_text`: reject at `qr-text`, before contributing an equation or establishing a transfer. These cases exercise alphabet, length, overflow, whitespace, and resource-limit checks. Do not normalize the text to make it valid.
- `routing_vectors`: choose the stated parser before validating its payload. In particular, `D+9` routes unsupported versions and flags to the fountain parser without falling back to a token or UR parser. A routing example is not necessarily a valid transfer.

For a QR integration check, render `qr_text` in alphanumeric mode, scan it through a text API, and compare the returned string exactly. Then Base45-decode it and compare with `frame_hex`. A version 10-M symbol fits a 207-byte frame (183 fragment bytes) as 311 characters; a 208-byte frame needs 312 characters and does not fit that symbol in alphanumeric mode.

## Receiver sequences

`receiver_sequences` supplies ordered `steps` for a fresh decoder. A `receive` step contains equivalent binary and QR text forms. `result` is `incomplete`, `complete`, or `reject`; `reject_at: "transfer"` means the frame is individually valid but belongs to a different transfer tuple. Successful completion yields the sequence's `message_hex`.

The `reject-unrelated` policy selects the spec's single-session option: reject an unrelated frame while retaining the active session. Implementations with multiple sessions or automatic session switching can instead verify that the unrelated equation never enters the original reconstruction.

The failed-reconstruction sequence introduces a bad equation first, with a valid frame checksum. The final equation reveals the message-checksum failure. No successful result is produced; an explicit `reset` step discards all accumulated equations before a clean retry. This also works with implementations that reset automatically after reconstruction failure.
