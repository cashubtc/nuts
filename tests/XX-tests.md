# NUT-XX Test Vectors

Keys and tags are as in the [NUT-10 vectors](10-tests.md). Signatures are BIP-340 with the auxiliary randomness fixed to 32 zero bytes; verifiers **MUST** accept any valid signature. Each string is the prefix plus base64url (no padding) of the JSON shown. Decoders parse the JSON; its byte form varies by encoder.

## Signing package

The [NUT-00 mint vector](00-tests.md#transaction-transcripts) with its quote locked to a script-only key, NUMS offset `u = 7` with one `threshold` leaf `n = 1` for key `3`, so the quote input spends through that leaf:

```json
{
  "lock_key": "034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af276",
  "transcript": "12003d0100010802000f71756f74652d6d696e742d30303031030021034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af27604000021004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "33d8def7c0f5235c150863773e105568d44d079aa2f1d59149bb72254dc6df05",
  "input_id": "a639745001afaad8964370e8ddc1406bbf14d478c6d56819f188c9b10392fe45",
  "input_digest": "7c0b3967b3b7ba4e5daa7e8ea11607cff36062d6ff24863c8bdf31ee8346f8e4"
}
```

The package, with one spend awaiting signatures on input `0`:

```json
{
  "version": "nutspA",
  "transcript": "12003d0100010802000f71756f74652d6d696e742d30303031030021034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af27604000021004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "spends": [
    {
      "input": 0,
      "secret": "034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af276",
      "leaf": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
      "control": {
        "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
        "path": []
      },
      "signatures": []
    }
  ]
}
```

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjEyMDAzZDAxMDAwMTA4MDIwMDBmNzE3NTZmNzQ2NTJkNmQ2OTZlNzQyZDMwMzAzMDMxMDMwMDIxMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2MDQwMDAwMjEwMDRiMDEwMDAxMDgwMjAwMjEwMjI1NDZhYjBhMmRlZTlmNzk1MTBmNGUyMGE0ZTNkOWU4OTRhOTczNjEwNDdjNTk0OTAyNTczYTdlNjRmOWQ3MDEwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIiwic3BlbmRzIjpbeyJpbnB1dCI6MCwic2VjcmV0IjoiMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2IiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOSIsImNvbnRyb2wiOnsiSyI6IjAyOGVkZmViZDZmZGVhM2UxZDg5MzU5YWYyMDg2OGEyZTc2MzE1YjM2Y2RiMWE3OWRlNDk3YTE3NTdjYTdiZDQwNyIsInBhdGgiOltdfSwic2lnbmF0dXJlcyI6W119XX0
```

Signed by key `3` over `input_digest`:

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjEyMDAzZDAxMDAwMTA4MDIwMDBmNzE3NTZmNzQ2NTJkNmQ2OTZlNzQyZDMwMzAzMDMxMDMwMDIxMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2MDQwMDAwMjEwMDRiMDEwMDAxMDgwMjAwMjEwMjI1NDZhYjBhMmRlZTlmNzk1MTBmNGUyMGE0ZTNkOWU4OTRhOTczNjEwNDdjNTk0OTAyNTczYTdlNjRmOWQ3MDEwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIiwic3BlbmRzIjpbeyJpbnB1dCI6MCwic2VjcmV0IjoiMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2IiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOSIsImNvbnRyb2wiOnsiSyI6IjAyOGVkZmViZDZmZGVhM2UxZDg5MzU5YWYyMDg2OGEyZTc2MzE1YjM2Y2RiMWE3OWRlNDk3YTE3NTdjYTdiZDQwNyIsInBhdGgiOltdfSwic2lnbmF0dXJlcyI6WyJiMDY1NmRiZGUxNDNiZDY4MjVlMTQxNTUxY2FlNjhmMTQyOGE2MmVlMWQ3NGMwZjhkZjhmNzM1ZDU4NDE0NzFkNmYyMGYzOTQ2NjU4YmRhZDIyNWI2YjMwZGM5MGNlYTk1NmEwYWVkZTEzMmVkZjZlYjE0MTVmOTVhZmIzMGNhMiJdfV19
```

which merges into the quote input's witness:

```json
{
  "leaf": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": []
  },
  "signatures": [
    "b0656dbde143bd6825e141551cae68f1428a62ee1d74c0f8df8f735d5841471d6f20f3946658bdad225b6b30dc90cea956a0aede132edf6eb1415f95afb30ca2"
  ]
}
```
