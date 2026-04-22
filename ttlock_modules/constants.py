from enum import StrEnum


class LockProvider(StrEnum):
    TTLOCK = "ttlock"
    SCIENER = "sciener"


TTLOCK_API_BASE_URL = "https://api.ttlock.com"
SCIENER_API_BASE_URL = "https://api.sciener.com"

PROVIDER_BASE_URLS = {
    LockProvider.TTLOCK: TTLOCK_API_BASE_URL,
    LockProvider.SCIENER: SCIENER_API_BASE_URL,
}
