from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

def generate_keypair():
    """Generate an X25519 key pair"""
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def hybrid_encrypt(recipient_pub_hex, plaintext: bytes):
    """Hybrid encryption using: ephemeral key + X25519 + AES-GCM"""
    recipient_pub = x25519.X25519PublicKey.from_public_bytes(bytes.fromhex(recipient_pub_hex))
    ephemeral_sk = x25519.X25519PrivateKey.generate()
    shared_key = ephemeral_sk.exchange(recipient_pub)

    aesgcm = AESGCM(shared_key[:32])
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return {
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ephemeral_pub": ephemeral_sk.public_key().public_bytes_raw().hex()
    }

def hybrid_decrypt(recipient_sk, enc_data):
    """Decrypt AES-GCM ciphertext using recipient's private key"""
    eph_pub = x25519.X25519PublicKey.from_public_bytes(bytes.fromhex(enc_data["ephemeral_pub"]))
    shared_key = recipient_sk.exchange(eph_pub)
    aesgcm = AESGCM(shared_key[:32])
    nonce = base64.b64decode(enc_data["nonce"])
    ciphertext = base64.b64decode(enc_data["ciphertext"])
    return aesgcm.decrypt(nonce, ciphertext, None)
