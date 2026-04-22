from .client import LockClient
from .constants import LockProvider


class TTLockClient(LockClient):
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
    ):
        super().__init__(
            provider=LockProvider.TTLOCK,
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            access_token=access_token,
        )


class ScienerClient(LockClient):
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
    ):
        super().__init__(
            provider=LockProvider.SCIENER,
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            access_token=access_token,
        )
