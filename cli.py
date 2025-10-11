import argparse
import json
import time
from tx_block import Transaction, sha256_hex
from node import Node
from crypto_utils import generate_keypair, hybrid_encrypt, hybrid_decrypt
from cryptography.hazmat.primitives.asymmetric import x25519

def save_keys_to_file(private_key, public_key, filename="keys.json"):
    """Save key pair to a JSON file"""
    data = {
        "private": private_key.private_bytes_raw().hex(),
        "public": public_key.public_bytes_raw().hex()
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"🔑 Keys saved to {filename}")

def run_keygen(args):
    sk, pk = generate_keypair()
    save_keys_to_file(sk, pk)
    print(f"Private key: {sk.private_bytes_raw().hex()}")
    print(f"Public key: {pk.public_bytes_raw().hex()}")

def run_send(args):
    node = Node(difficulty=2, chain_file="chain.json")

    # Load sender's key pair
    with open("keys.json", "r") as f:
        my_keys = json.load(f)

    from_pk = my_keys["public"]
    to_pk = args.to_enc_pk_hex
    plaintext = args.msg.encode("utf-8")

    # Encrypt message
    enc_meta = hybrid_encrypt(to_pk, plaintext)

    payload = {
        "from": from_pk,
        "to": to_pk,
        "ciphertext": enc_meta["ciphertext"],
        "cipher_meta": {
            "nonce": enc_meta["nonce"],
            "ephemeral_pub": enc_meta["ephemeral_pub"]
        },
        "payload_hash": sha256_hex(args.msg),
        "timestamp": int(time.time())
    }

    tx = Transaction(payload)
    node.add_transaction(tx)
    node.mine_block()
    print("✅ Blockchain updated and saved to chain.json")

def run_read(args):
    node = Node(difficulty=2, chain_file="chain.json")

    with open("keys.json", "r") as f:
        my_keys = json.load(f)
    sk = x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(my_keys["private"]))

    with open("chain.json", "r") as f:
        chain = json.load(f)

    found = False
    for block in chain[1:]:
        for tx in block["transactions"]:
            plaintext = node.read_transaction(tx, sk)
            if plaintext:
                print(f"✅ Decrypted message: {plaintext}")
                found = True
    if not found:
        print("❌ No decryptable transactions found")

def main():
    parser = argparse.ArgumentParser(description="🪙 ChatChain - Encrypted Blockchain Messaging CLI")
    sub = parser.add_subparsers()

    p1 = sub.add_parser("keygen", help="Generate key pair")
    p1.set_defaults(func=run_keygen)

    p2 = sub.add_parser("send", help="Send encrypted message")
    p2.add_argument("--to_enc_pk_hex", required=True, help="Recipient's encryption public key")
    p2.add_argument("--msg", required=True, help="Message to send")
    p2.set_defaults(func=run_send)

    p3 = sub.add_parser("read", help="Decrypt messages from the blockchain")
    p3.set_defaults(func=run_read)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
