# Organizer Notes

## Challenge summary
- Name: Layered Lunch
- Category: Crypto
- Difficulty: Easy
- Player task:
  1. Decode Base64 ten times.
  2. Recover the MD5 hash.
  3. Crack the hash using a known password database / wordlist (Like rockyou.txt or CrackStation)
  4. Submit the flag as `GIUCTF{plaintext}`.

## Embedded MD5
`bae48f3fe501adbf257b19a897d2bee9`

## Files
- `generator.py`: regenerates `challenge.txt` from the chosen MD5 hash.
- `solver.py`: unwraps the ten Base64 layers and prints the final MD5 hash.

## Recommended pre-release check
Confirm that the chosen MD5 resolves to the intended plaintext in the lookup source or wordlist you expect teams to use.
