# Author Notes

## Summary
This is a RSA challenge based on the classic non-invertible RSA mistake. (https://eprint.iacr.org/2020/1059.pdf)

The public exponent is `e = 17`, but both primes are generated so that:

```text
(p - 1) % e^2 == 0
(q - 1) % e^2 == 0
```

As a result, `gcd(e, phi(N)) = 17`, so the usual RSA private exponent does not exist.
Encryption is many-to-one, and decrypting the ciphertext means recovering all possible
17th roots modulo `p` and modulo `q`, then combining them with CRT.


## Intended solve
1. Notice from `generate.py` that `e` divides both `p - 1` and `q - 1`.
2. Factor `N`.
3. Compute all solutions to:

```text
x^17 = cipher mod p
x^17 = cipher mod q
```

4. Combine every pair of roots with CRT.
5. Convert candidates to bytes and search for `GIUCTF{`.

## Parameters
```text
p = 265304105653268360976755876206305002833
q = 172653595315864605033815610513630877073
N = 45805707693096782568413911567752028022821344516902403143900673627661539747809
e = 17
cipher = 39478420966026085254469258545208682382442235779624354482946817348207310495436
```

## Flag
```text
GIUCTF{many_rsa_roots}
```

## Notes
- `N` is intentionally small enough for a CTF crypto challenge.
- The author solver uses SymPy for modular nth roots and CRT. (You can use Sage aswell)
