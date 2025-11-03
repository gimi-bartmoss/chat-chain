# modules

## `crypto_utils.py`

A lightweight **hybrid encryption** scheme combining **X25519 key exchange** and **AES-GCM symmetric encryption**.
Each encryption uses a new ephemeral key, providing high efficiency and **forward secrecy**.

For detailed explanation, see [`docs/crypto_utils.md`](docs/crypto_utils.md).

## `tx_block.py`

This module implements a **minimal blockchain structure** — including transactions, blocks, and a proof-of-work mechanism.

