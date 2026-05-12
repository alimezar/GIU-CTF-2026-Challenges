# Patience — Timing Oracle CTF Challenge

This package contains a live timing-oracle crypto challenge.

## Folder layout

```txt
for_players/   Files to give contestants
service/       Python oracle service for local testing/deployment
authors/       Solver, generator, and challenge notes
```

## Local setup

From the package root:

```bash
cd service
python3 app.py
```

The service will listen on:

```txt
http://127.0.0.1:5000
```

Quick check:

```bash
curl "http://127.0.0.1:5000/check?key=A"
```

Expected response:

```json
{"ok":false}
```

## Fast local smoke test

To test the full solve more quickly, lower the delay:

```bash
cd service
ORACLE_DELAY_MS=10 ORACLE_JITTER_MS=5 python3 app.py
```

Then in another terminal:

```bash
cd authors
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python solve.py --url http://127.0.0.1:5000 --output ../for_players/output.txt
```

## Default challenge timing

Default service settings:

```txt
ORACLE_DELAY_MS=60
ORACLE_JITTER_MS=30
ORACLE_LOCK_MODE=ip
```

This intentionally makes the solve take time even when the player understands the vulnerability.

## Docker setup

```bash
cd service
docker build -t patience-oracle .
docker run --rm -p 5000:5000 patience-oracle
```

With explicit secret and timing settings:

```bash
docker run --rm -p 5000:5000 \
  -e ORACLE_SECRET_KEY='Wa1t_F0r_The_B33p!' \
  -e ORACLE_DELAY_MS=60 \
  -e ORACLE_JITTER_MS=30 \
  patience-oracle
```

## Player release

Only give players:

```txt
for_players/README.md
for_players/output.txt
oracle URL
```

Do not give players `service/` or `authors/`.
