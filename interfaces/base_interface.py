import inspect

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class BaseInterface:
    """Shared primitives used by all domain-specific interfaces."""

    def __init__(self, interface):
        """Store root interface/client object for subsequent API operations."""
        self.interface = interface
        self.client = interface

    async def _ensure_login(self) -> None:
        """Ensure access token exists, invoking login() when needed."""
        if getattr(self.client, "access_token", None):
            return

        login = getattr(self.interface, "login", None)
        if login is None:
            raise ValueError(
                "No access token provided and interface.login() is unavailable."
            )

        result = login()
        if inspect.isawaitable(result):
            await result

        if not getattr(self.client, "access_token", None):
            raise ValueError("Login completed without access token.")

    def _normalize_date(self, value: int | datetime | str | None) -> int | None:
        """Normalize optional date-like values to millisecond timestamps."""
        if value is None:
            return None
        return self.client._date_to_timestamp(value)

    def _prepare_payload(self, data: dict[str, Any] | BaseModel) -> dict[str, Any]:
        """Prepare request payload while dropping None-valued business fields."""
        if isinstance(data, BaseModel):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = {key: value for key, value in data.items() if value is not None}
        return self.client._prepare_api_payload(payload)
