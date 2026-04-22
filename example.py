import asyncio
from lock import Lock

from settings import settings

ttlock = Lock(
    client_id=settings.TTLOCK_CLIENT_ID,
    client_secret=settings.TTLOCK_CLIENT_SECRET,
    username=settings.TTLOCK_USERNAME,
    password=settings.TTLOCK_PASSWORD,
)


if __name__ == "__main__":
    print(asyncio.run(ttlock.Lock.get_detail(lock_id=30074580)))