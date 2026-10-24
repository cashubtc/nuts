# NUT-XX Test Vectors

Keys and tags are as in the [NUT-10 vectors](10-tests.md). Signatures are BIP-340 with the auxiliary randomness fixed to 32 zero bytes; verifiers **MUST** accept any valid signature. Each string is the prefix plus base64url (no padding) of the JSON shown. Decoders parse the JSON; its byte form varies by encoder.

## Signing package

The [NUT-00 mint vector](00-tests.md#transaction-transcripts) with its quote locked to a script-only key, NUMS offset `u = 7` with one `threshold` leaf `n = 1` for key `3`, so the quote input spends through that leaf:

```json
{
  "lock_key": "034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af276",
  "transcript": "12003d0100010802000f71756f74652d6d696e742d30303031030021034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af27604000021004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "1b6a4f3f56d3808cb81d176a5f9959ebe5dc9251de66056794000ad758a9eb84",
  "input_id": "a639745001afaad8964370e8ddc1406bbf14d478c6d56819f188c9b10392fe45",
  "input_digest": "1e0acf51dc92e81c87ad238eea380c8238373aee3e2a30167547ce20c9212a50"
}
```

The package, with one spend awaiting signatures on input `0`:

```json
{
  "version": "nutspA",
  "transcript": "12003d0100010802000f71756f74652d6d696e742d30303031030021034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af27604000021004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
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
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjEyMDAzZDAxMDAwMTA4MDIwMDBmNzE3NTZmNzQ2NTJkNmQ2OTZlNzQyZDMwMzAzMDMxMDMwMDIxMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2MDQwMDAwMjEwMDRiMDEwMDAxMDgwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIiwic3BlbmRzIjpbeyJpbnB1dCI6MCwic2VjcmV0IjoiMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2IiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOSIsImNvbnRyb2wiOnsiSyI6IjAyOGVkZmViZDZmZGVhM2UxZDg5MzU5YWYyMDg2OGEyZTc2MzE1YjM2Y2RiMWE3OWRlNDk3YTE3NTdjYTdiZDQwNyIsInBhdGgiOltdfSwic2lnbmF0dXJlcyI6W119XX0
```

Signed by key `3` over `input_digest`:

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjEyMDAzZDAxMDAwMTA4MDIwMDBmNzE3NTZmNzQ2NTJkNmQ2OTZlNzQyZDMwMzAzMDMxMDMwMDIxMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2MDQwMDAwMjEwMDRiMDEwMDAxMDgwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIiwic3BlbmRzIjpbeyJpbnB1dCI6MCwic2VjcmV0IjoiMDM0YjE1MTI5YTljNjY1ZjM3ZmJlOWY2YzgwYTdmZTZlYzBjODA5ZjM0ZWRkZTk4ZDI5OGFmZjk0YTFlOGFmMjc2IiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOSIsImNvbnRyb2wiOnsiSyI6IjAyOGVkZmViZDZmZGVhM2UxZDg5MzU5YWYyMDg2OGEyZTc2MzE1YjM2Y2RiMWE3OWRlNDk3YTE3NTdjYTdiZDQwNyIsInBhdGgiOltdfSwic2lnbmF0dXJlcyI6WyIxMWVkYWYzNjA4YTZiMWZiZWMxOWYxODI2ZTU4YWNlMDljYTUxYWFmYmI3YWQxMTJhMGIwYjhmODc4Nzk2N2Q5OGVlYTI5MzZiYjU1MDUzZGQ0NjNkYmU0N2MyZjIzZjM3ZTU0NzVhZTRlYmU5MmIzMjhkZjU0ZTgwYzdkOTIwNiJdfV19
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
    "11edaf3608a6b1fbec19f1826e58ace09ca51aafbb7ad112a0b0b8f8787967d98eea2936bb55053dd463dbe47c2f23f37e5475ae4ebe92b328df54e80c7d9206"
  ]
}
```
