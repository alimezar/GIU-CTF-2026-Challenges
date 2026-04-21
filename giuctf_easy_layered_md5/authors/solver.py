import base64

with open("../for_players/challenge.txt", "rb") as f:
    data = f.read().strip()

for i in range(10):
    data = base64.b64decode(data)
    print(f"After decode {i+1}: {data[:80]!r}")

print("Final:", data.decode())
