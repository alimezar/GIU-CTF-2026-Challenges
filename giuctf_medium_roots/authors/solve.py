#!/usr/bin/env python3
"""
Author solver for many-roots.

Dependencies:
    pip install sympy

The challenge can also be solved in Sage using nth_root(..., all=True).
"""

from sympy.ntheory.residue_ntheory import nthroot_mod
from sympy.ntheory.modular import crt

N = 45805707693096782568413911567752028022821344516902403143900673627661539747809
e = 17
cipher = 39478420966026085254469258545208682382442235779624354482946817348207310495436

# Author-known factorization.
# Players are expected to factor N themselves first, via FactorDB or similar.
p = 265304105653268360976755876206305002833
q = 172653595315864605033815610513630877073

def long_to_bytes(n):
    n = int(n)
    if n == 0:
        return b"\x00"
    return n.to_bytes((n.bit_length() + 7) // 8, "big")

def main():
    roots_p = nthroot_mod(cipher, e, p, True)
    roots_q = nthroot_mod(cipher, e, q, True)

    print(f"[+] roots modulo p: {len(roots_p)}")
    print(f"[+] roots modulo q: {len(roots_q)}")

    hits = []
    for rp in roots_p:
        for rq in roots_q:
            candidate = int(crt([p, q], [int(rp), int(rq)])[0])
            candidate_bytes = long_to_bytes(candidate)

            if candidate_bytes.startswith(b"GIUCTF{"):
                hits.append(candidate_bytes)

    if not hits:
        print("[-] no GIUCTF flag found")
        return

    for hit in hits:
        print(hit.decode(errors="replace"))

if __name__ == "__main__":
    main()
