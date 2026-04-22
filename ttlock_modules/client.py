import hashlib
import time
from datetime import datetime
from typing import Optional

import httpx
import pytz
from pydantic import BaseModel, SecretStr

from settings import settings

from .constants import PROVIDER_BASE_URLS, LockProvider
from .exceptions import LockAPIError


class LockClientTools:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.http_client.aclose()

    def _get_current_millis(self) -> int:
        return int(time.time() * 1000)

    def _prepare_api_payload(
        self,
        data: Optional[str | BaseModel] = None,
        response_model: Optional[BaseModel] = None,
    ) -> dict:
        payload = {
            "clientId": self.client_id,
            "accessToken": self.access_token,
            "date": self._get_current_millis(),
        }
        if isinstance(data, BaseModel):
            data = data.model_dump()
        if data:
            payload.update(data)

        if response_model is not None:
            response_model(**payload)
        return payload

    def _date_to_timestamp(self, dt: int | datetime | str) -> int:
        if isinstance(dt, int):
            return dt
        if isinstance(dt, datetime):
            if dt.tzinfo is None:
                dt = pytz.timezone("Europe/Moscow").localize(dt)
            return int(dt.timestamp() * 1000)
        if isinstance(dt, str):
            try:
                parsed = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = pytz.timezone("Europe/Moscow").localize(parsed)
                return int(parsed.timestamp() * 1000)
            except Exception:
                raise ValueError(f"Invalid date format: {dt}")
        raise ValueError(f"Unsupported date type: {type(dt)}")


class LockClient(LockClientTools):
    def __init__(
        self,
        provider: LockProvider = LockProvider.TTLOCK,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
    ):
        self.provider = provider
        self.api_base_url = PROVIDER_BASE_URLS[provider]

        client_secret_value = (
            client_secret.get_secret_value()
            if isinstance(client_secret, SecretStr)
            else client_secret
        )
        password_value = (
            password.get_secret_value() if isinstance(password, SecretStr) else password
        )

        self.client_id = client_id or settings.TTLOCK_CLIENT_ID
        self.client_secret = client_secret_value or settings.TTLOCK_CLIENT_SECRET
        self.username = username or settings.TTLOCK_USERNAME
        self.password = password_value or (
            settings.TTLOCK_PASSWORD.get_secret_value()
            if isinstance(settings.TTLOCK_PASSWORD, SecretStr)
            else settings.TTLOCK_PASSWORD
        )
        if self.password and not self.password.startswith("md5"):
            self.password = hashlib.md5(self.password.encode("utf-8")).hexdigest()
        self.access_token = access_token

        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def request(self, method: str, endpoint: str, data: dict | None = None):
        """Internal method to make HTTP requests using the persistent session."""
        url = (
            f"{self.api_base_url}{endpoint}"
            if not endpoint.startswith("http")
            else endpoint
        )

        try:
            response = await self.http_client.request(
                method, url, data=data, headers=self.headers
            )
            response.raise_for_status()
            resp_data = response.json()
        except httpx.HTTPStatusError as e:
            try:
                error_body = e.response.json()
                raise LockAPIError(
                    f"HTTP Error {e.response.status_code}: {error_body}",
                    e.response.status_code,
                )
            except Exception:
                raise LockAPIError(
                    f"HTTP Error {e.response.status_code}", e.response.status_code
                )
        except Exception as e:
            raise LockAPIError(str(e))

        if (
            isinstance(resp_data, dict)
            and "errcode" in resp_data
            and resp_data["errcode"] != 0
        ):
            raise LockAPIError(
                resp_data.get("errmsg", "Unknown error"), resp_data["errcode"]
            )

        return resp_data
