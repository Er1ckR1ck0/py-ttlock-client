from typing import Optional

from py_ttlock_client.client import LockClient
from py_ttlock_client.modules.constants import LockProvider


class TTLockClient(LockClient):
    """Provider-specific client wrapper for TTLock endpoints."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        """Initialize a LockClient preconfigured for the TTLock provider."""
        super().__init__(
            provider=LockProvider.TTLOCK,
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            access_token=access_token,
        )


class ScienerClient(LockClient):
    """Provider-specific client wrapper for Sciener endpoints."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        """Initialize a LockClient preconfigured for the Sciener provider."""
        super().__init__(
            provider=LockProvider.SCIENER,
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            access_token=access_token,
        )
