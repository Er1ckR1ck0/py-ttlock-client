from datetime import datetime
from typing import Any, Mapping

from ttlock_modules.constants import ENDPOINTS
from ttlock_modules.schemas.qr import (
    CyclicConfig,
    QRCodeCreateResponse,
    QRCodeData,
    QRCodeListRequest,
    QRCodeListResponse,
)

from ttlock_modules.interfaces.base_interface import BaseInterface

QR_ENDPOINTS = {
    "add": ENDPOINTS["qrcode_add"],
    "list": ENDPOINTS["qrcode_get_all"],
    "get": ENDPOINTS["qrcode_get_one"],
    "delete": "/v3/qrCode/delete",
    "update": "/v3/qrCode/update",
    "clear": "/v3/qrCode/clear",
}


class QRInterface(BaseInterface):
    async def create(
        self,
        lock_id: int,
        qr_type: int,
        *,
        name: str | None = None,
        start_date: int | datetime | str | None = None,
        end_date: int | datetime | str | None = None,
        cyclic_config: list[CyclicConfig | Mapping[str, Any]] | None = None,
    ) -> QRCodeCreateResponse:
        await self._ensure_login()
        payload = self.client._prepare_api_payload(
            {
                "lockId": lock_id,
                "type": qr_type,
                "name": name,
                "startDate": self._normalize_date(start_date),
                "endDate": self._normalize_date(end_date),
                "cyclicConfig": self._normalize_cyclic_config(cyclic_config),
            }
        )
        return await self.client.request(
            "POST",
            QR_ENDPOINTS["add"],
            data=payload,
            response_model=QRCodeCreateResponse,
        )

    async def get_list(
        self,
        lock_id: int,
        page: int = 1,
        page_size: int = 20,
        *,
        name: str | None = None,
    ) -> QRCodeListResponse:
        await self._ensure_login()
        payload = self.client._prepare_api_payload(
            QRCodeListRequest(
                lockId=lock_id, pageNo=page, pageSize=page_size, name=name
            ).model_dump()
        )
        return await self.client.request(
            "POST",
            QR_ENDPOINTS["list"],
            data=payload,
            response_model=QRCodeListResponse,
        )

    async def get(self, code_id: int) -> QRCodeData:
        await self._ensure_login()
        payload = self.client._prepare_api_payload({"qrCodeId": code_id})
        return await self.client.request(
            "GET",
            QR_ENDPOINTS["get"],
            params=payload,
            response_model=QRCodeData,
        )

    async def delete(self, lock_id: int, code_id: int) -> dict[str, Any]:
        await self._ensure_login()
        payload = self.client._prepare_api_payload(
            {
                "lockId": lock_id,
                "qrCodeId": code_id,
            }
        )
        return await self.client.request("POST", QR_ENDPOINTS["delete"], data=payload)

    async def update(
        self,
        code_id: int,
        *,
        name: str | None = None,
        start_date: int | datetime | str | None = None,
        end_date: int | datetime | str | None = None,
        cyclic_config: list[CyclicConfig | Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        await self._ensure_login()
        payload = self.client._prepare_api_payload(
            {
                "qrCodeId": code_id,
                "name": name,
                "startDate": self._normalize_date(start_date),
                "endDate": self._normalize_date(end_date),
                "cyclicConfig": self._normalize_cyclic_config(cyclic_config),
            }
        )
        return await self.client.request("POST", QR_ENDPOINTS["update"], data=payload)

    async def clear(self, lock_id: int) -> dict[str, Any]:
        await self._ensure_login()
        payload = self.client._prepare_api_payload({"lockId": lock_id})
        return await self.client.request("POST", QR_ENDPOINTS["clear"], data=payload)
