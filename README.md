# modules

## `crypto_utils.py`

A lightweight **hybrid encryption** scheme combining **X25519 key exchange** and **AES-GCM symmetric encryption**.
Each encryption uses a new ephemeral key, providing high efficiency and **forward secrecy**.

| Function | Description |
|-----------|-------------|
| `generate_keypair()` | Generate an X25519 key pair. |
| `hybrid_encrypt(pub_hex, plaintext)` | Encrypt with ephemeral key + AES-GCM. |
| `hybrid_decrypt(sk, enc_data)` | Decrypt and verify message integrity. |

For detailed explanation, see [`docs/encryption.md`](docs/encryption.md).
