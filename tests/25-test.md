# NUT-25 Test Vectors

The following list of items should encode to the target filter `z4fUCDVqdnxWR7Y9+YdT5o0IC9GxiSA2BGyg`, with parameters:

- `p = 19`
- `m = 784931`

```json
[
  "c2735796c1d45c68e7f03d3ea3bfcf5d6f10e6eb480e57fc3dccaf8ce66990dfc5",
  "3c7ac2a233f8d5439be8cf3109d314e7da476e1ca762dc05f64ca3d5acac2da1fa",
  "73e199a811db202ef7fbb1699b0e4859d15735c8f7f838fd9e50b37dc47c0ff4b9",
  "02f171db2b577f6d586580651da4951c2e1506454bb9b76077d7a9fdb8606cf2f6",
  "106954852453d217ad91e3b14c37bcb6adf62b038cc6a6a281f63edf78de2c7819",
  "621e006de8d41b14491933e695985a730179003846b739224316af578fc49c1ee8",
  "59b759ecda3c4d9027b9fe549fe6ae33b1bf573b9e9c2d0cdf17d20ea38794f1b7",
  "cfcc8745503e9efb67e48b0bee006f6433dec534130707ac23ed4eae911d60eec2",
  "f1d57d98f80e528af885e6174f7cd0ef39c31f8436c66b8f27c848a3497c9a7dfb",
  "5a21aa11ccd643042f3fe3f0fcc02ccfb51c72419c5eab64a3565aa8499aa64cdf"
]
```

Matching any given item from this list should return `True`, while matching any item from the following list
should return `False`:
```json
[
  "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3",
  "d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6",
  "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",
  "ffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100ffee",
  "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c"
]
```
