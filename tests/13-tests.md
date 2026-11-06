# NUT-13 Test vectors

## Version 3: Secret derivation

Using [NUT-13](../13.md#v3-message) derivation procedure for V3 with the following inputs, the seed given as its 64 bytes rather than a mnemonic:

```json
{
  "seed_hex": "6e757431332076332074657374207365656400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "keyset_id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701"
}
```

The values derived for counters `0` to `3` are:

```json
[
  {
    "counter": 0,
    "secret_key": "930c88ad9dc8531c147862d4ef9c0981200ff1f510c0a9e1c024db725a1d56c6",
    "secret": "0240c186f3e19f6f8cd00db81c5266d5c74ddca48ff848efd0e3e125b2846f30d9",
    "blinding_factor": "4381a54d5fb006bf9cd63a30e857f0ef4b58a5a123c7cd8909099abe77d5736e",
    "nums_offset": "c4b697b346799e55a80ba7a0b6f7670a7f62a985c97de685dc693e87dc6d137a",
    "Y": "90f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8"
  },
  {
    "counter": 1,
    "secret_key": "a2ac179175fc3bb7c8cf05542193017a0d33b3316ea5d8a97777c7660d2a55b6",
    "secret": "0385fe6eb0608c6b5241e0fd86ebbd5dd30a6a97a0014a110c0c6297001147e5be",
    "blinding_factor": "2349fa461401f98e1ffa80d34baf1c11bbe62014bbd076985229f0706cda83f1",
    "nums_offset": "1b864ba8bba906c1bd1b56e58c1b0fe4ee8d3bea42849309102c81a8854f312d"
  },
  {
    "counter": 2,
    "secret_key": "fec1f9c77a85ea144b6ea2ecd90a61a226855b4ed692a7e8c7db7afb600f7205",
    "secret": "0390617487ad222beef9f247dbfbd5993313a2d5235add388bd868969c594794a2",
    "blinding_factor": "7121cd4ce638011afaea356eefe1834b03a86080064c7c28f1eab45c32d7b06e",
    "nums_offset": "b19ab48593e7ad6fc3c68c23697b6b2544920a1949ca234a6d10a2cdb6455922"
  },
  {
    "counter": 3,
    "secret_key": "1aa7018e67ac4655d3d6dd120a2c715adb6bcd6b54dbf90a685ae452916edb61",
    "secret": "039e49f114e0ab5f616b996e93f04ae265e29282df093c08996c093f1fcbb4385f",
    "blinding_factor": "46186ec0f98f00aaf51a7cb59472c65e35a33f94e2785b6b384d1666b9c1759c",
    "nums_offset": "3ee8a5612ad8ff4a6f5b7bcf5b6bef7c7a2379fc789401e8e03afbf32da6dfad"
  }
]
```

For counters `0` to `3` the `0x00` branch accepts at attempts `0, 0, 0, 0` and the `0x01` branch at attempts `0, 3, 0, 1` (earlier attempts produce `x >= BLS_FR_ORDER`). An implementation that omits the loop, skips the length framing, or reuses the V2 message computes different values and fails these vectors.

Counter `0` also carries `Y = hash_to_curve_G1(secret_bytes)` over the **decoded 33 bytes** of the secret, pinning the binary-secret hashing rule ([NUT-00](../00.md#secret-bytes)).

The **leaf keys** (type `0x03`) at counter `0`, with the index suffix `u32_BE(i)`:

```json
[
  {
    "counter": 0,
    "index": 0,
    "privkey": "e6573de10fb740e60350346f7a90e15dfff01efb476c745018f59b6ab5132644",
    "pubkey": "036ed2c40140c79e5080a15e88cb55f7c08c0107b465cfef8ddcfe66a2ba3532f9"
  },
  {
    "counter": 0,
    "index": 1,
    "privkey": "2ab582bed4c0a4c0d746b8bfbe906cf7d7becf88f4dfe66cd194851c64d44bb1",
    "pubkey": "0369e4632867bd810a4a7065494b48c7fda2dd6ec4eba4fd93ce545bd32d5c45df"
  },
  {
    "counter": 0,
    "index": 2,
    "privkey": "520f39607492fad03cf0b2c44929680ef3b0955adf20a9b2d9b64b18bffaeaa4",
    "pubkey": "037864253663cfeadc8bd3d5d573ca1858378951bbd7fe971712940f38c4c47c86"
  }
]
```

**NOTE**:`i` is not a leaf's position: recover by deriving candidates and matching the tree's keys by value.

Type `0x04` (quote lock key) frames the mint's [NUT-06](../06.md) identity `pubkey` as `scope_bytes` instead of a keyset id, and has a quote counter of its own. With the same seed and the NUT-06 example identity:

```json
{
  "mint_pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da"
}
```

```json
[
  {
    "counter": 0,
    "privkey": "8140af6b627ddf38f9148c7266dca12d396de9266859648df699727c5b205a99",
    "pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812"
  },
  {
    "counter": 1,
    "privkey": "5980da641d9391abed79f528dbea0b85a61cff419bc93bce744d105779413b7a",
    "pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d"
  }
]
```
