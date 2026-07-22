from collections import defaultdict
from datetime import datetime, timedelta, timezone

FAILED_LOGIN_ATTEMPTS = defaultdict(list)

MAX_FAILED_ATTEMPTS = 6
WINDOW_SECONDS = 60


def _now():
    return datetime.now(timezone.utc)


def prune_old_attempts(ip_address: str) -> None:
    cutoff = _now() - timedelta(seconds=WINDOW_SECONDS)
    FAILED_LOGIN_ATTEMPTS[ip_address] = [
        attempt_time
        for attempt_time in FAILED_LOGIN_ATTEMPTS[ip_address]
        if attempt_time > cutoff
    ]


def get_failed_attempt_count(ip_address: str) -> int:
    prune_old_attempts(ip_address)
    return len(FAILED_LOGIN_ATTEMPTS[ip_address])


def record_failed_attempt(ip_address: str) -> int:
    prune_old_attempts(ip_address)
    FAILED_LOGIN_ATTEMPTS[ip_address].append(_now())
    return len(FAILED_LOGIN_ATTEMPTS[ip_address])


def clear_failed_attempts(ip_address: str) -> None:
    FAILED_LOGIN_ATTEMPTS.pop(ip_address, None)