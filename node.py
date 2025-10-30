import json
import os
from tx_block import Block, Transaction
from crypto_utils import hybrid_decrypt

class Node:
    """Blockchain node core: handles transaction pool, mining, and chain storage"""
    def __init__(self, difficulty=2, chain_file="chain.json"):
        self.difficulty = difficulty
        self.chain_file = chain_file

        if os.path.exists(self.chain_file):
            with open(self.chain_file, "r") as f:
                self.chain = json.load(f)
        else:
            self.chain = []
            self._create_genesis()
            self._save_chain()

        self.mempool = []

    def _create_genesis(self):
        """Create the genesis block"""
        genesis = Block(0, "0" * 64, [], self.difficulty)
        genesis.mine()
        self.chain.append(genesis.to_dict())

    def _save_chain(self):
        """Persist the blockchain to a file"""
        with open(self.chain_file, "w") as f:
            json.dump(self.chain, f, indent=2, ensure_ascii=False)

    def add_transaction(self, tx: Transaction):
        """Add a transaction object to the mempool"""
        self.mempool.append(tx)

    def mine_block(self):
        """Package transactions from mempool and perform mining"""
        if not self.mempool:
            print("No transactions to mine")
            return

        prev_hash = self.chain[-1]["hash"]
        block = Block(
            index=len(self.chain),
            prev_hash=prev_hash,
            transactions=self.mempool,
            difficulty=self.difficulty
        )

        block.mine()
        self.chain.append(block.to_dict())
        self._save_chain()
        self.mempool.clear()

    def read_transaction(self, tx_dict, recipient_sk):
        """Decrypt a transaction from the blockchain"""
        try:
            enc_data = {
                "ciphertext": tx_dict["ciphertext"],
                "nonce": tx_dict["cipher_meta"]["nonce"],
                "ephemeral_pub": tx_dict["cipher_meta"]["ephemeral_pub"]
            }
            plaintext = hybrid_decrypt(recipient_sk, enc_data)
            return plaintext.decode("utf-8")
        except Exception as e:
            print("Decryption error:", e)
            return None
