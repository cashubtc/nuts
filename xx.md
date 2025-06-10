# NUT-XX: Nostr Mint Backup

`optional`

---

This document describes a method for wallets to backup their mint list as ephemeral Nostr events on one or more relays. This allows users to restore their mint configuration across different devices or wallet instances using their mnemonic seed phrase.

## Description

Wallet users can optionally enable backup of their mint list to Nostr relays. The mint list is encrypted using NIP-44 encryption and published as replaceable Nostr events. The backup keys are deterministically derived from the wallet's mnemonic seed phrase, ensuring that the same seed can restore the mint list on any compatible wallet.

## Key Derivation

The private key for Nostr mint backup is derived from the wallet's mnemonic seed phrase using the following method:

1. Generate a 64-byte seed from the mnemonic using BIP39 `mnemonicToSeedSync(mnemonic)`
2. Create a domain separator: `UTF-8("cashu-mint-backup")`
3. Concatenate the seed and domain separator: `combined_data = seed || domain_separator`
4. Hash the combined data: `private_key = SHA256(combined_data)`
5. Derive the public key: `public_key = secp256k1_generator * private_key`

### Example Implementation

```javascript
import { mnemonicToSeedSync } from "@scure/bip39";
import { sha256 } from "@noble/hashes/sha256";
import { bytesToHex } from "@noble/hashes/utils";
import { getPublicKey } from "nostr-tools";

function deriveMintBackupKeys(mnemonic: string): { privateKeyHex: string; publicKeyHex: string } {
  // Derive seed from mnemonic
  const seed: Uint8Array = mnemonicToSeedSync(mnemonic);
  const domainSeparator = new TextEncoder().encode("cashu-mint-backup");
  const combinedData = new Uint8Array(seed.length + domainSeparator.length);
  combinedData.set(seed);
  combinedData.set(domainSeparator, seed.length);

  // Use SHA256 of combined data as private key
  const privateKeyBytes = sha256(combinedData);
  const privateKeyHex = bytesToHex(privateKeyBytes);
  const publicKeyHex = getPublicKey(privateKeyBytes);

  return { privateKeyHex, publicKeyHex };
}
```

## Nostr Event Specification

### Event Kind

The mint backup uses Nostr event kind `30078` (replaceable event) as specified in [NIP-78](https://github.com/nostr-protocol/nips/blob/master/78.md).

### Event Structure

```json
{
  "kind": 30078,
  "content": "<encrypted_backup_data>",
  "tags": [
    ["d", "mint-list"],
    ["client", "cashu.me"]
  ],
  "created_at": <timestamp>,
  "pubkey": "<mint_backup_public_key>"
}
```

### Event Fields

- `kind`: **MUST** be `30078` (replaceable event)
- `content`: Encrypted mint backup data using NIP-44 encryption
- `tags`: 
  - `d` tag with value `"mint-list"` (replaceable event identifier)
  - `client` tag with the client name (optional but recommended)
- `created_at`: Unix timestamp of the backup creation
- `pubkey`: The derived public key for mint backup

### Backup Data Format

The plaintext data that gets encrypted in the `content` field has the following JSON structure:

```json
{
  "mints": ["<mint_url_1>", "<mint_url_2>", ...],
  "timestamp": <unix_timestamp>
}
```

### Encryption

The backup data is encrypted using NIP-44 v2 encryption:

1. Generate a conversation key using NIP-44: `conversation_key = nip44.v2.utils.getConversationKey(private_key, public_key)`
2. Encrypt the JSON string: `encrypted_content = nip44.v2.encrypt(JSON.stringify(backup_data), conversation_key)`
3. Use the encrypted content as the event's `content` field

Note: The same private and public key pair is used for both sides of the conversation key generation, creating a self-encrypted message.

## Wallet Implementation

### Backup Flow

1. **Enable Backup**: User enables Nostr mint backup in wallet settings
2. **Key Derivation**: Wallet derives backup keys from the mnemonic seed
3. **Data Preparation**: Wallet collects current mint URLs and creates backup data structure
4. **Encryption**: Backup data is encrypted using NIP-44 v2
5. **Event Creation**: Create Nostr event with encrypted content and appropriate tags
6. **Publishing**: Sign and publish the event to configured Nostr relays

### Restore Flow

1. **Key Derivation**: Derive backup keys from the provided mnemonic seed
2. **Event Discovery**: Search for events with:
   - `kind`: `30078`
   - `authors`: `[<derived_public_key>]`
   - `#d`: `["mint-list"]`
3. **Decryption**: Decrypt event content using NIP-44 v2
4. **Mint Addition**: Present discovered mints to user for selective restoration

### Example Backup Event

```json
{
  "id": "...",
  "kind": 30078,
  "content": "AgAQJBIqWKEEBjGHfoozgDBgVQAAAAC5lQJtJQV_psHckN2KxWsUq7Q-B_twv4M2P3_vJrPMWg",
  "tags": [
    ["d", "mint-list"],
    ["client", "cashu.me"]
  ],
  "created_at": 1703721600,
  "pubkey": "02bc9097997d81afb2cc7346b5e4345a9346bd2a506eb7958598a72f0cf85163ea",
  "sig": "..."
}
```

When decrypted, the content would reveal:

```json
{
  "mints": [
    "https://mint.example.com",
    "https://another-mint.org"
  ],
  "timestamp": 1703721600
}
```

[00]: 00.md
[01]: 01.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[07]: 07.md
[08]: 08.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md