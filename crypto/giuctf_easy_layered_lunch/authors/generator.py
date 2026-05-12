import base64

hash_text = b"bae48f3fe501adbf257b19a897d2bee9"

data = hash_text
for _ in range(10):
    data = base64.b64encode(data)

with open("challenge.txt", "wb") as f:
    f.write(data)

print(data.decode())
