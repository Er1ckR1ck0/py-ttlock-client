from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from modules.constants import ENDPOINTS
from interfaces.base_interface import BaseInterface
from schemas.lock import (
    LockAutoLockTimeRequest,
    LockBatteryUpdateRequest,
    LockDetail,
    LockIdRequest,
    LockListRequest,
    LockListResponse,
    LockOpenStateResponse,
    LockOperationResponse,
    LockRenameRequest,
    LockTransferRequest,
)

LOCK_ENDPOINTS = {
    "list": ENDPOINTS["lock_list"],
    "detail": ENDPOINTS["lock_detail"],
    "lock": ENDPOINTS["lock_lock"],
    "unlock": ENDPOINTS["lock_unlock"],
    "rename": ENDPOINTS["lock_rename"],
    "delete": ENDPOINTS["lock_delete"],
    "transfer": ENDPOINTS["lock_transfer"],
    "query_open_state": ENDPOINTS["lock_query_open_state"],
    "set_auto_lock_time": ENDPOINTS["lock_set_auto_lock_time"],
    "update_electric_quantity": ENDPOINTS["lock_update_electric_quantity"],
    "freeze": ENDPOINTS["lock_freeze"],
    "unfreeze": ENDPOINTS["lock_unfreeze"],
}


class LockInterface(BaseInterface):
    """Interface for TTLock lock management endpoints."""

    async def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any],
        response_model: type[BaseModel] | None = None,
    ) -> Any:
        response = await self.client.request(method, endpoint, data=payload)
        if response_model is None:
            return response
        return response_model.model_validate(response)

    async def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        *,
        lock_alias: str | None = None,
        device_type: int | None = None,
        group_id: int | None = None,
    ) -> LockListResponse:
        """
        Get paginated list of all locks in the account.

        Args:
            page: Page number (starts from 1).
            page_size: Items per page (default 20, max 10000).
            lock_alias: Filter by alias (fuzzy match).
            device_type: 1=lock (default), 2=lift controller.
            group_id: Filter by group.
        """
        await self._ensure_login()
        payload = self._prepare_payload(
            LockListRequest(
                lockAlias=lock_alias,
                type=device_type,
                groupId=group_id,
                pageNo=page,
                pageSize=page_size,
            )
        )
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["list"],
            payload,
            LockListResponse,
        )

    async def get_detail(self, lock_id: int) -> LockDetail:
        """
        Get full lock details including firmware, battery, features, keys, etc.

        Args:
            lock_id: The lock ID.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["detail"],
            payload,
            LockDetail,
        )

    async def lock(self, lock_id: int) -> LockOperationResponse:
        """
        Send remote lock command via gateway.

        Args:
            lock_id: The lock ID.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["lock"],
            payload,
            LockOperationResponse,
        )

    async def unlock(self, lock_id: int) -> LockOperationResponse:
        """
        Send remote unlock command via gateway.
        Note: Remote Unlock must be enabled in the TTLock app settings.

        Args:
            lock_id: The lock ID.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["unlock"],
            payload,
            LockOperationResponse,
        )

    async def rename(self, lock_id: int, alias: str) -> LockOperationResponse:
        """
        Change the lock alias (display name).

        Args:
            lock_id: The lock ID.
            alias: New name for the lock.
        """
        await self._ensure_login()
        payload = self._prepare_payload(
            LockRenameRequest(lockId=lock_id, lockAlias=alias)
        )
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["rename"],
            payload,
            LockOperationResponse,
        )

    async def delete(self, lock_id: int) -> LockOperationResponse:
        """
        Remove the lock from the account. Requires admin rights.

        Args:
            lock_id: The lock ID.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["delete"],
            payload,
            LockOperationResponse,
        )

    async def transfer(
        self, lock_id: int, receiver_username: str
    ) -> LockOperationResponse:
        """
        Transfer lock ownership to another account.

        Args:
            lock_id: The lock ID.
            receiver_username: Username of the receiving account.
        """
        await self._ensure_login()
        payload = self._prepare_payload(
            LockTransferRequest(
                lockId=lock_id, receiverUsername=receiver_username
            )
        )
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["transfer"],
            payload,
            LockOperationResponse,
        )

    async def query_open_state(self, lock_id: int) -> LockOpenStateResponse:
        """
        Query the current door state (locked / unlocked / unknown).

        Args:
            lock_id: The lock ID.

        Returns:
            LockOpenStateResponse with state: 0=locked, 1=unlocked, 2=unknown.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["query_open_state"],
            payload,
            LockOpenStateResponse,
        )

    async def set_auto_lock_time(
        self,
        lock_id: int,
        seconds: int,
        *,
        via_gateway: bool = True,
    ) -> LockOperationResponse:
        """
        Set auto-lock delay.

        Args:
            lock_id: The lock ID.
            seconds: Auto-lock delay in seconds. Use -1 to disable.
            via_gateway: True = via gateway (type=2), False = via BLE (type=1).
        """
        await self._ensure_login()
        payload = self._prepare_payload(
            LockAutoLockTimeRequest(
                lockId=lock_id,
                seconds=seconds,
                type=2 if via_gateway else 1,
            )
        )
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["set_auto_lock_time"],
            payload,
            LockOperationResponse,
        )

    async def update_battery(
        self, lock_id: int, electric_quantity: int
    ) -> LockOperationResponse:
        """
        Upload current battery level (obtained from SDK) to the server.

        Args:
            lock_id: The lock ID.
            electric_quantity: Battery level (0–100).
        """
        await self._ensure_login()
        payload = self._prepare_payload(
            LockBatteryUpdateRequest(
                lockId=lock_id, electricQuantity=electric_quantity
            )
        )
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["update_electric_quantity"],
            payload,
            LockOperationResponse,
        )

    async def freeze(self, lock_id: int) -> LockOperationResponse:
        """
        Freeze (disable) the lock remotely.

        Args:
            lock_id: The lock ID.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["freeze"],
            payload,
            LockOperationResponse,
        )

    async def unfreeze(self, lock_id: int) -> LockOperationResponse:
        """
        Unfreeze (re-enable) the lock remotely.

        Args:
            lock_id: The lock ID.
        """
        await self._ensure_login()
        payload = self._prepare_payload(LockIdRequest(lockId=lock_id))
        return await self._request(
            "POST",
            LOCK_ENDPOINTS["unfreeze"],
            payload,
            LockOperationResponse,
        )
