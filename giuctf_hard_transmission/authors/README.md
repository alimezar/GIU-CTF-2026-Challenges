# The Last Transmission

## Challenge Summary

This is a WW2-themed Hard cryptography challenge based on the Enigma machine.

Players are given the intercepted ciphertext:

```text
pskhq owdfi uerwr njzlv cszok nrwdd lfaxo qttla uvsgn yk
```

The intended plaintext is:

```text
OPERATIONNIGHTFALLHASBEENEXPOSEDWELLDONESOLDIER
```

The flag should be derived from the plaintext according to the public challenge rules, for example:

```text
GIUCTF{OPERATION_NIGHTFALL_HAS_BEEN_EXPOSED_WELL_DONE_SOLDIER}
```

## Generator

https://cryptii.com/pipes/enigma-machine/

## Enigma Settings

Use the following settings:

```text
Model: Enigma M3
Reflector: UKW B
Rotors: VII II V
Ring settings: A A A
Starting positions: A Q L
Plugboard: BQ CR DI EJ KW MT OS PX UZ GH
```

Important: the rotor order is `VII II V`. Rings, starting positions, reflector, and plugboard must remain exactly as listed above.

## Intended Solve Path

1. Recognize that the grouped ciphertext is an Enigma-style message.
2. Use an Enigma simulator or a Python Enigma library.
3. Configure the machine with:
   - Reflector B
   - Rotors VII II V
   - Ring settings A A A
   - Starting positions A Q L
   - Plugboard BQ CR DI EJ KW MT OS PX UZ GH
4. Remove spaces from the ciphertext before processing if using `py-enigma`.
5. Decrypt the ciphertext to recover:

```text
OPERATIONNIGHTFALLHASBEENEXPOSEDWELLDONESOLDIER
```

6. Convert the message into the expected flag format.

## Additional Notes

- If using `py-enigma`, strip spaces from the ciphertext before decrypting. Leaving spaces in may produce incorrect output depending on how the library processes input.
- The challenge is not meant to be difficult once the correct Enigma settings are found; the main puzzle is identifying the machine and applying the exact configuration.
- Surprisingly, AI struggles with this challenge.
