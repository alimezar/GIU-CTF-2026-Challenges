#!/usr/bin/env python3
import json
import os
import random
import secrets
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


SECRET_ORACLE_KEY = os.environ.get("ORACLE_SECRET_KEY")

if not SECRET_ORACLE_KEY:
    raise RuntimeError(
        "Missing ORACLE_SECRET_KEY. Set it in the deployment environment."
    )


DELAY_MS = float(os.environ.get("ORACLE_DELAY_MS", "70"))
JITTER_MS = float(os.environ.get("ORACLE_JITTER_MS", "40"))
MAX_GUESS_LEN = int(os.environ.get("ORACLE_MAX_GUESS_LEN", "128"))

# ip     = one active request per client IP
# global = one active request total
# off    = no locking, mostly for debugging
LOCK_MODE = os.environ.get("ORACLE_LOCK_MODE", "ip").lower()

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))

_locks = {}
_locks_guard = threading.Lock()
_global_lock = threading.Lock()


def insecure_timing_check(guess: str) -> bool:
    """
    Intentionally vulnerable.

    The checker sleeps once for every correct prefix character.
    Good things come to those who wait.
    """

    for i in range(min(len(guess), len(SECRET_ORACLE_KEY))):
        if guess[i] != SECRET_ORACLE_KEY[i]:
            break

        time.sleep(DELAY_MS / 1000.0)

    if JITTER_MS > 0:
        time.sleep(random.uniform(0, JITTER_MS) / 1000.0)

    return secrets.compare_digest(guess, SECRET_ORACLE_KEY)


class Handler(BaseHTTPRequestHandler):
    server_version = "PatienceOracle/1.2"

    def log_message(self, fmt, *args):
        return

    def client_id(self):
        forwarded = self.headers.get("X-Forwarded-For", "")
        if forwarded:
            return forwarded.split(",")[0].strip()

        real_ip = self.headers.get("X-Real-IP", "")
        if real_ip:
            return real_ip.strip()

        return self.client_address[0]

    def get_lock(self):
        if LOCK_MODE == "off":
            return None

        if LOCK_MODE == "global":
            return _global_lock

        cid = self.client_id()

        with _locks_guard:
            lock = _locks.get(cid)

            if lock is None:
                lock = threading.Lock()
                _locks[cid] = lock

            return lock

    def send_json(self, data, status=HTTPStatus.OK):
        body = json.dumps(data, separators=(",", ":")).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self.send_json(
                {
                    "challenge": "Patience",
                    "message": "Good things come to those who wait.",
                    "usage": "/check?key=<guess>",
                }
            )

        if parsed.path == "/healthz":
            return self.send_json({"ok": True})

        if parsed.path != "/check":
            return self.send_json(
                {"ok": False, "error": "not found"},
                HTTPStatus.NOT_FOUND,
            )

        qs = parse_qs(parsed.query, keep_blank_values=True)
        guess = qs.get("key", [""])[0]

        if len(guess) > MAX_GUESS_LEN:
            return self.send_json(
                {"ok": False, "error": "guess too long"},
                HTTPStatus.BAD_REQUEST,
            )

        lock = self.get_lock()
        acquired = True

        if lock is not None:
            acquired = lock.acquire(blocking=False)

            if not acquired:
                return self.send_json(
                    {"ok": False, "error": "one request at a time, please"},
                    HTTPStatus.TOO_MANY_REQUESTS,
                )

        try:
            ok = insecure_timing_check(guess)
            return self.send_json({"ok": ok})
        finally:
            if lock is not None and acquired:
                lock.release()


def main():
    print(f"Patience oracle listening on http://{HOST}:{PORT}", flush=True)
    print(
        f"delay={DELAY_MS}ms jitter=0-{JITTER_MS}ms "
        f"lock_mode={LOCK_MODE} max_guess_len={MAX_GUESS_LEN}",
        flush=True,
    )

    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()