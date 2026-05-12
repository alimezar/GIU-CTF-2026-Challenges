#!/usr/bin/env python3
import argparse
import re
import statistics
import time
from hashlib import sha256
from pathlib import Path

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


DEFAULT_CHARSET = "".join(chr(i) for i in range(33, 127))
VAULT_ID = b"patience-v2"


def timed_check(session: requests.Session, base_url: str, guess: str):
    url = base_url.rstrip("/") + "/check"

    while True:
        start = time.perf_counter()
        response = session.get(url, params={"key": guess}, timeout=30)
        elapsed = time.perf_counter() - start

        if response.status_code == 429:
            time.sleep(0.1)
            continue

        response.raise_for_status()
        return elapsed, bool(response.json().get("ok"))


def recover_ticket(
    base_url: str,
    charset: str,
    max_len: int,
    refine_top: int,
    refine_samples: int,
):
    session = requests.Session()
    known = ""

    for pos in range(max_len):
        timings = []

        for ch in charset:
            guess = known + ch
            elapsed, ok = timed_check(session, base_url, guess)

            if ok:
                return guess

            timings.append((elapsed, ch))

        timings.sort(reverse=True)
        finalists = timings[:refine_top]

        scored = []

        for _, ch in finalists:
            samples = []

            for _ in range(refine_samples):
                guess = known + ch
                elapsed, ok = timed_check(session, base_url, guess)

                if ok:
                    return guess

                samples.append(elapsed)

            scored.append((statistics.median(samples), ch, samples))

        scored.sort(reverse=True)
        best_score, best_ch, samples = scored[0]
        known += best_ch

        rounded = [round(s, 4) for s in samples]
        print(
            f"[{pos + 1:02d}] {known!r}  "
            f"median={best_score:.4f}s samples={rounded}",
            flush=True,
        )

        elapsed, ok = timed_check(session, base_url, known)

        if ok:
            return known

    raise RuntimeError("Reached max length without finding an accepted ticket.")


def parse_output(path: str):
    text = Path(path).read_text(encoding="utf-8")

    nonce_match = re.search(r"nonce\s*=\s*([0-9a-fA-F]+)", text)
    sealed_match = re.search(r"sealed\s*=\s*([0-9a-fA-F]+)", text)

    if not nonce_match or not sealed_match:
        raise ValueError("Could not parse output.txt")

    nonce = bytes.fromhex(nonce_match.group(1))
    sealed = bytes.fromhex(sealed_match.group(1))

    return nonce, sealed


def decrypt_flag(output_path: str, ticket: str):
    nonce, sealed = parse_output(output_path)
    key = sha256(ticket.encode()).digest()

    return AESGCM(key).decrypt(nonce, sealed, VAULT_ID)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:5000",
        help="Base URL of the oracle service",
    )
    parser.add_argument(
        "--output",
        default="../for_players/output.txt",
        help="Path to output.txt",
    )
    parser.add_argument(
        "--charset",
        default=DEFAULT_CHARSET,
        help="Characters to try at each position",
    )
    parser.add_argument(
        "--max-len",
        type=int,
        default=64,
        help="Maximum ticket length to attempt",
    )
    parser.add_argument(
        "--refine-top",
        type=int,
        default=6,
        help="Number of candidates to resample per position",
    )
    parser.add_argument(
        "--refine-samples",
        type=int,
        default=3,
        help="Number of timing samples for each finalist",
    )

    args = parser.parse_args()

    ticket = recover_ticket(
        base_url=args.url,
        charset=args.charset,
        max_len=args.max_len,
        refine_top=args.refine_top,
        refine_samples=args.refine_samples,
    )

    print("ticket =", ticket)

    flag = decrypt_flag(args.output, ticket)
    print("flag =", flag.decode())


if __name__ == "__main__":
    main()