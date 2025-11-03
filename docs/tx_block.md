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

# Flowchart

```mermaid
flowchart TD
    A[Start] --> B[Create Transaction Objects]
    B --> C[Collect Transactions into List]
    C --> D["Initialize Block (index, prev_hash, transactions, difficulty)"]
    D --> E["Block.to_dict() → Build Block Data Structure"]
    E --> F[Begin Mining Loop]
    
    subgraph Mining_Process
        F --> G[Convert Block to JSON String]
        G --> H[Compute SHA-256 Hash]
        H --> I{Hash starts with N zeros?}
        I -->|Yes| J[Set block.hash = hash_val]
        I -->|No| K[Increment nonce]
        K --> F
    end

    J --> L[Mining Complete]
    L --> M[Return Valid Mined Block]
    M --> N[End]

