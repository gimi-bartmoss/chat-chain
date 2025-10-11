import time
import hashlib
import json

def sha256_hex(obj):
    """Compute SHA-256 hash of an object (supports string or JSON)"""
    if isinstance(obj, bytes):
        obj = obj.decode("utf-8", errors="ignore")
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class Transaction:
    """Transaction object that encapsulates transaction data"""
    def __init__(self, payload):
        self.payload = payload

    def to_dict(self):
        return self.payload


class Block:
    """Block object containing transactions, previous hash, difficulty, and mining logic"""
    def __init__(self, index, prev_hash, transactions, difficulty=2, nonce=0):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = int(time.time())
        self.difficulty = difficulty
        self.nonce = nonce
        self.transactions = [tx.to_dict() for tx in transactions]  # list of transactions
        self.hash = None

    def to_dict(self):
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "hash": self.hash
        }

    def mine(self):
        """Simple proof-of-work: find a nonce such that hash starts with a given number of zeros"""
        prefix = "0" * self.difficulty
        while True:
            block_string = json.dumps(self.to_dict(), sort_keys=True)
            hash_val = hashlib.sha256(block_string.encode("utf-8")).hexdigest()
            if hash_val.startswith(prefix):
                self.hash = hash_val
                break
            self.nonce += 1
