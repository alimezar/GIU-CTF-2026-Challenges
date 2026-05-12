# Author Notes

## Summary

This is a live timing-oracle challenge.

Players get a sealed vault, a small opener script, and an oracle endpoint:

```txt
/check?key=<guess>
```

The endpoint compares guesses against a secret ticket character-by-character and sleeps after every correct prefix character. The intended solve is to recover the ticket through timing, then use it with `vault.py` to open the sealed output.

## Flag

```txt
GIUCTF{P@tience_1s_4_V1rtu3_but_W@1t!}
```

## Oracle ticket

```txt
qJ9~v_Rm-2!sXkA7.pZ4
```

Do not use a word-like ticket. Keep this random-looking.

## Railway environment

Set these variables:

```txt
ORACLE_SECRET_KEY=qJ9~v_Rm-2!sXkA7.pZ4
ORACLE_DELAY_MS=70
ORACLE_JITTER_MS=40
ORACLE_LOCK_MODE=ip
ORACLE_MAX_GUESS_LEN=128
```

## Expected solve time

With the default author solver, printable visible ASCII, length 20, 70 ms delay, and 40 ms jitter, the solve should land around 20–25 minutes.

Rough timing:

```txt
94 candidates × sum(0..19) × 70 ms ≈ 20.8 minutes
```

Refinement samples and jitter push it slightly higher.


## Local test

Terminal 1:

```bash
cd service
ORACLE_SECRET_KEY='qJ9~v_Rm-2!sXkA7.pZ4' \
ORACLE_DELAY_MS=10 \
ORACLE_JITTER_MS=5 \
python3 app.py
```

Terminal 2:

```bash
cd authors
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 solve.py --url http://127.0.0.1:5000 --output ../for_players/output.txt
```

Use the fast local delay only for testing. Use the real Railway delay for the official challenge.