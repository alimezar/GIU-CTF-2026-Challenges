# Another Angle v2

## Intended solve path
1. Read `shelf.txt`.
2. The clue line suggests a non-straight reading.
3. The main diagonal of the 10x10 grid gives the XOR key: `sp1nef0ld7`.
4. The anti-diagonal `dustj4cket` and the first-column string `endpapers1` are decoys / alternate plausible reads.
5. Base64-decode `cipher.txt`.
6. Repeating-key XOR with key `sp1nef0ld7`. Possible Hint can be added for this step
7. The plaintext is a chunky block-ASCII rendering of the full flag.
8. Read the banner.

## Final flag
`GIUCTF{sl4nt3dsh3lv3s84}`
