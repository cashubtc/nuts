# NUT-19 Test Vectors

The following is a `PostMintBolt11Request` with a valid signature. Where the `pubkey` in the `PostMintQuoteBolt11Request` is `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac`.

```json
{
  "quote": "9d745270-1405-46de-b5c5-e2762b4f5e00",
  "outputs": [],
  "witness": "d9be080b33179387e504bb6991ea41ae0dd715e28b01ce9f63d57198a095bccc776874914288e6989e97ac9d255ac667c205fa8d90a211184b417b4ffdd24092"
}
```

The following is a `PostMintBolt11Request` with an invalid signature. Where the `pubkey` in the `PostMintQuoteBolt11Request` is `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac`.

```json
{
  "quote": "9d745270-1405-46de-b5c5-e2762b4f5e00",
  "outputs": [],
  "witness": "cb2b8e7ea69362dfe2a07093f2bbc319226db33db2ef686c940b5ec976bcbfc78df0cd35b3e998adf437b09ee2c950bd66dfe9eb64abd706e43ebc7c669c36c3"
}
```
