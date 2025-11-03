# tx_block.py

## Overview
This module defines the basic units of a blockchain:
- `Transaction`: encapsulates transaction data.
- `Block`: contains transactions, previous hash, mining difficulty, and proof-of-work logic.

---

## Functions and Classes

### `sha256_hex(obj)`
Computes the SHA-256 hash of an object (serialized as JSON for consistency).

---

### `class Transaction`
**Initialization:**
```python
Transaction(payload: dict)
```
**Methods:**
- `to_dict()`: returns the transaction as a dictionary.

---

### `class Block`
**Initialization:**
```python
Block(index, prev_hash, transactions, difficulty=2, nonce=0)
```

Attributes:
- `index`: block height  
- `prev_hash`: hash of the previous block  
- `transactions`: list of transaction dictionaries  
- `difficulty`: mining difficulty (number of leading zeros)  
- `nonce`: random integer used for mining  
- `hash`: computed block hash  

**Methods:**
- `to_dict()`: returns block information as a dictionary.  
- `mine()`: performs a simple proof-of-work algorithm by finding a hash that meets the difficulty target.

---

## Applications
This module can serve as the foundation of a blockchain system, supporting:
- Block validation and chain linking
- Proof-of-Work simulation

## Architecture Diagram

```mermaid
classDiagram
    direction TB

    class sha256_hex {
        +sha256_hex(obj)
        calculate SHA-256
    }

    class Transaction {
        -payload : dict
        +__init__(payload)
        +to_dict() dict
    }

    class Block {
        -index : int
        -prev_hash : str
        -timestamp : int
        -transactions : list
        -difficulty : int
        -nonce : int
        -hash : str
        +__init__(index, prev_hash, transactions, difficulty, nonce)
        +to_dict() dict
        +mine() None
    }

    sha256_hex <.. Block : uses
    Transaction --> Block : "transactions list"
