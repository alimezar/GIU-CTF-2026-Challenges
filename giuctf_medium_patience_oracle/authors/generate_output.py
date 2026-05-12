#!/usr/bin/env python3
import os
import secrets
from hashlib import sha256

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


FLAG = os.environ.get(
    "FLAG",
    "GIUCTF{P@tience_1s_4_V1rtu3_but_W@1t!}",
).encode()

ORACLE_KEY = os.environ.get("ORACLE_SECRET_KEY")
VAULT_ID = os.environ.get("VAULT_ID", "patience-v2").encode()

if not ORACLE_KEY:
    raise RuntimeError("Set ORACLE_SECRET_KEY before generating output.txt")

nonce_hex = os.environ.get("NONCE_HEX")

if nonce_hex:
    NONCE = bytes.fromhex(nonce_hex)
else:
    NONCE = secrets.token_bytes(12)

key = sha256(ORACLE_KEY.encode()).digest()
sealed = AESGCM(key).encrypt(NONCE, FLAG, VAULT_ID)

print("# The box refuses to explain itself.")
print()
print("nonce =", NONCE.hex())
print("sealed =", sealed.hex())