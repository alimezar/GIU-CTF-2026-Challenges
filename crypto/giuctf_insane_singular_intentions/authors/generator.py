#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import secrets
from pathlib import Path
from typing import List

DEFAULT_FLAG = "GIUCTF{gr0ebn3r_b4s1s+s4g3!}"
DEFAULT_BITS = 1024
DEFAULT_E = 41  # early prime so the brute-force solver reaches it quickly


def bytes_to_long(data: bytes) -> int:
    return int.from_bytes(data, "big")


def small_primes_upto(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            start = i * i
            sieve[start:n + 1:i] = [False] * (((n - start) // i) + 1)
    return [i for i, ok in enumerate(sieve) if ok]


SMALL_PRIMES = small_primes_upto(10000)
VALID_E_VALUES = [p for p in small_primes_upto(1023) if p >= 3]  # exclude 2


def is_probable_prime(n: int, rounds: int = 24) -> bool:
    if n < 2:
        return False

    for p in SMALL_PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits: int, e: int) -> int:
    """Generate a prime p such that gcd(e, p-1) == 1."""
    if bits < 16:
        raise ValueError("bits must be at least 16")

    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1))
        candidate |= 1
        if math.gcd(e, candidate - 1) != 1:
            continue
        if is_probable_prime(candidate):
            return candidate


def split_flag_into_three_chunks(flag: bytes) -> List[bytes]:
    if not flag.startswith(b"GIUCTF{") or not flag.endswith(b"}"):
        raise ValueError("Flag must be in GIUCTF{...} format.")

    base, extra = divmod(len(flag), 3)
    sizes = [base + (1 if i < extra else 0) for i in range(3)]

    out = []
    idx = 0
    for size in sizes:
        chunk = flag[idx:idx + size]
        idx += size
        if not chunk:
            raise ValueError("All three chunks must be non-empty.")
        out.append(chunk)
    return out


def write_secret_py(path: Path, pts: List[bytes], p: int, q: int) -> None:
    path.write_text(
        f"pts = {pts!r}\n"
        f"p = {p}\n"
        f"q = {q}\n",
        encoding="utf-8",
    )


def write_output_txt(path: Path, pts: List[bytes], p: int, q: int, e: int) -> None:
    N = p * q
    pt_ints = [bytes_to_long(x) for x in pts]
    cts = [pow(m, e, N) for m in pt_ints]
    hint = sum(pt_ints)
    path.write_text(f"{N},{cts},{hint}\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a valid quick maffs instance.")
    parser.add_argument("--flag", default=DEFAULT_FLAG, help="Flag in GIUCTF{...} format.")
    parser.add_argument("--bits", type=int, default=DEFAULT_BITS, help="Bit length of each RSA prime.")
    parser.add_argument("--e", type=int, default=DEFAULT_E, help="Hidden prime exponent (<1024). Default: 41.")
    parser.add_argument("--out-dir", default=".", help="Where to write secret.py, output.txt, and author_info.json.")
    args = parser.parse_args()

    if args.e not in VALID_E_VALUES:
        raise ValueError("e must be an odd prime in [3, 1023].")

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    flag = args.flag.encode()
    pts = split_flag_into_three_chunks(flag)

    # Pick p and q so that gcd(e, phi(N)) = 1.
    p = gen_prime(args.bits, args.e)
    q = gen_prime(args.bits, args.e)
    while q == p:
        q = gen_prime(args.bits, args.e)

    secret_path = out_dir / "secret.py"
    output_path = out_dir / "output.txt"
    info_path = out_dir / "author_info.json"

    write_secret_py(secret_path, pts, p, q)
    write_output_txt(output_path, pts, p, q, args.e)

    info = {
        "flag": args.flag,
        "chunks_ascii": [chunk.decode("utf-8", errors="replace") for chunk in pts],
        "chunks_hex": [chunk.hex() for chunk in pts],
        "e": args.e,
        "bits_per_prime": args.bits,
    }
    info_path.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")

    print(f"[+] wrote {secret_path}")
    print(f"[+] wrote {output_path}")
    print(f"[+] wrote {info_path}")
    print(f"[+] hidden exponent e = {args.e}")
    print(f"[+] chunks = {info['chunks_ascii']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
