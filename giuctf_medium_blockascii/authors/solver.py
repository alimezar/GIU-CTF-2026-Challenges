import base64
from pathlib import Path

lines = [line.strip() for line in Path("shelf.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
grid = lines[1:]
key = ''.join(grid[i][i] for i in range(len(grid)))
print("Recovered key:", key)

data = base64.b64decode(Path("cipher.txt").read_text().strip())
plain = bytes(b ^ key.encode()[i % len(key)] for i, b in enumerate(data))
Path("decrypted_banner.txt").write_bytes(plain)
print(plain.decode("utf-8"))
