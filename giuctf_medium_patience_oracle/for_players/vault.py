#!/usr/bin/env python3
from getpass import getpass
from hashlib import sha256
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM as LittleLock
except ImportError:
    print("The lock is missing a tooth.")
    print("Try: python -m pip install cryptography")
    raise SystemExit(1)


VAULT_ID = b"patience-v2"


def read_box(path="output.txt"):
    crumbs = {}

    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        crumbs[key.strip()] = value.strip()

    try:
        nonce = bytes.fromhex(crumbs["nonce"])
        sealed = bytes.fromhex(crumbs["sealed"])
    except KeyError:
        raise SystemExit("The box is missing something important.")
    except ValueError:
        raise SystemExit("The box contains suspicious crumbs.")

    return nonce, sealed


def ticket_to_teeth(ticket):
    # A polite ticket goes in.
    # Something less polite comes out.
    return sha256(ticket.encode()).digest()


def open_vault(ticket, path="output.txt"):
    nonce, sealed = read_box(path)

    # The vault accepts no almosts, maybes, or heartfelt apologies.
    return LittleLock(ticket_to_teeth(ticket)).decrypt(nonce, sealed, VAULT_ID)


if __name__ == "__main__":
    ticket = getpass("ticket: ")

    try:
        print(open_vault(ticket).decode())
    except Exception:
        print("The vault stayed closed.")