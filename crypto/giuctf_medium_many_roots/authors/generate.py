#!/usr/bin/env python3
"""
Python generator used to create this GIUCTF challenge instance.

"""

import secrets
from math import gcd

def is_probable_prime(n, rounds=8):
    if n < 2:
        return False

    small_primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
        173, 179, 181, 191, 193, 197, 199
    ]

    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for _ in range(rounds):
        bases.append(secrets.randbelow(n - 3) + 2)

    for a in bases:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def get_annoying_prime(nbits, e):
    modulus = e * e
    low = (1 << (nbits - 1)) // modulus
    high = (1 << nbits) // modulus

    while True:
        k = secrets.randbelow(high - low) + low

        # modulus is odd, so k must be even for k*modulus + 1 to be odd.
        if k & 1:
            k += 1

        p = k * modulus + 1
        if p.bit_length() == nbits and is_probable_prime(p):
            return p

def bytes_to_long(data):
    return int.from_bytes(data, "big")

def main():
    nbits = 128
    e = 17

    p = get_annoying_prime(nbits, e)
    q = get_annoying_prime(nbits, e)
    while p == q:
        q = get_annoying_prime(nbits, e)

    flag = b"GIUCTF{many_rsa_roots}"
    N = p * q
    cipher = pow(bytes_to_long(flag), e, N)

    print(f"p = {p}")
    print(f"q = {q}")
    print(f"N = {N}")
    print(f"e = {e}")
    print(f"cipher = {cipher}")
    print(f"gcd(e, phi) = {gcd(e, (p - 1) * (q - 1))}")

if __name__ == "__main__":
    main()
