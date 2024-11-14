# NUT-19 Test Vectors

The following is a `PostMintBolt11Request` with a valid signature. Where the `pubkey` in the `PostMintQuoteBolt11Request` is `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac`.

```json
{
  "quote": "9d745270-1405-46de-b5c5-e2762b4f5e00",
  "outputs": [
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "0342e5bcc77f5b2a3c2afb40bb591a1e27da83cddc968abdc0ec4904201a201834"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "032fd3c4dc49a2844a89998d5e9d5b0f0b00dde9310063acb8a92e2fdafa4126d4"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "033b6fde50b6a0dfe61ad148fff167ad9cf8308ded5f6f6b2fe000a036c464c311"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "02be5a55f03e5c0aaea77595d574bce92c6d57a2a0fb2b5955c0b87e4520e06b53"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "02209fc2873f28521cbdde7f7b3bb1521002463f5979686fd156f23fe6a8aa2b79"
    }
  ],
  "witness": "d4b386f21f7aa7172f0994ee6e4dd966539484247ea71c99b81b8e09b1bb2acbc0026a43c221fd773471dc30d6a32b04692e6837ddaccf0830a63128308e4ee0"
}
```

The following is the expected message to sign on the above `PostMintBolt11Request`.

```
9d745270-1405-46de-b5c5-e2762b4f5e000342e5bcc77f5b2a3c2afb40bb591a1e27da83cddc968abdc0ec4904201a201834032fd3c4dc49a2844a89998d5e9d5b0f0b00dde9310063acb8a92e2fdafa4126d4033b6fde50b6a0dfe61ad148fff167ad9cf8308ded5f6f6b2fe000a036c464c31102be5a55f03e5c0aaea77595d574bce92c6d57a2a0fb2b5955c0b87e4520e06b5302209fc2873f28521cbdde7f7b3bb1521002463f5979686fd156f23fe6a8aa2b79
```

The following is a `PostMintBolt11Request` with an invalid signature. Where the `pubkey` in the `PostMintQuoteBolt11Request` is `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac`.

```json
{
  "quote": "9d745270-1405-46de-b5c5-e2762b4f5e00",
  "outputs": [
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "0342e5bcc77f5b2a3c2afb40bb591a1e27da83cddc968abdc0ec4904201a201834"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "032fd3c4dc49a2844a89998d5e9d5b0f0b00dde9310063acb8a92e2fdafa4126d4"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "033b6fde50b6a0dfe61ad148fff167ad9cf8308ded5f6f6b2fe000a036c464c311"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "02be5a55f03e5c0aaea77595d574bce92c6d57a2a0fb2b5955c0b87e4520e06b53"
    },
    {
      "amount": 1,
      "id": "00456a94ab4e1c46",
      "B_": "02209fc2873f28521cbdde7f7b3bb1521002463f5979686fd156f23fe6a8aa2b79"
    }
  ],
  "witness": "cb2b8e7ea69362dfe2a07093f2bbc319226db33db2ef686c940b5ec976bcbfc78df0cd35b3e998adf437b09ee2c950bd66dfe9eb64abd706e43ebc7c669c36c3"
}
```
