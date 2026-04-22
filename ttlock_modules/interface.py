import asyncio
import logging

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional

from ttlock_modules.client import LockClient
from ttlock_modules.constants import ENDPOINTS
from ttlock_modules.exceptions import LockListNotExist
from ttlock_modules.schemas.qr import (
    CyclicConfig,
    QRCodeCreateResponse,
    QRCodeData,
    QRCodeListRequest,
    QRCodeListResponse,
)


class LockController:
    def __init__(self, client: LockClient):
        self.client = client
        if not all(
            [
                self.client.client_id,
                self.client.client_secret,
                self.client.username,
                self.client.password,
            ]
        ):
            raise ValueError(
                "Missing credentials for login (client_id, client_secret, username, password)"
            )

    async def login(self) -> None:
        if self.client.__dict__.get("access_token") is not None:
            return

        data = {
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "username": self.client.username,
            "password": self.client.password,
            "redirect_uri": "http://localhost:8000",
            "grant_type": "password",
        }

        response = await self.client.request(
            "POST", ENDPOINTS["oauth_token"], data=data
        )
        self.client.access_token = response.get("access_token")

    class __BaseType:
        def __init__(self, interface):
            self.interface = interface
            self.client = interface.client

    class _Locks(__BaseType):
        async def get_all_locks(
            self,
            lock_alias: Optional[str] = None,
            type: Optional[int] = None,
            group_id: Optional[int] = None,
            page_number: int = 1,
            page_size: int = 20,
        ) -> List[Dict]:
            """
            Get list of all locks in account.

            Args:
                clientId	String	Y	The app_id which is assigned by system when you create an application
                accessToken	String	Y	Access token
                lockAlias	String	N	Search by lock alias, fuzzy matching
                type	Int	N	Device type:1-lock, 2-Lift Controller, default 1
                groupId	Int	N	Group id
                pageNo	Int	Y	Page, start from 1
                pageSize	Int	Y	Items per page, default 20, max 10000
                date	Long	Y	Current time (timestamp in millisecond)

            Returns:
                list: all locks
            """
            payload = {
                "lockAlias": lock_alias,
                "type": type,
                "groupId": group_id,
                "pageNo": page_number,
                "pageSize": page_size,
            }
            full_payload = self.client._prepare_api_payload(payload)

            result = await self.client.request(
                "POST", ENDPOINTS["lock_list"], data=full_payload
            )
            lock_list = result.get("list", None)

            if not lock_list:
                raise LockListNotExist
            return [lock for lock in lock_list]

    class _Passcode(__BaseType):
        async def create_passcode(
            self,
            lock_id: int,
            name: str,
            start_date: int | datetime,
            end_date: int | datetime,
            passcode: str | int,
            add_type: int = 2,
        ) -> dict:
            """
            Creates a custom passcode (keyboard password).

            :param lock_id: The ID of the lock.
            :param name: Name for the passcode.
            :param start_date: Start time (timestamp in milliseconds or datetime object).
            :param end_date: End time (timestamp in milliseconds or datetime object).
            :param passcode: Passcode for locks
            :param add_type: Adding method:1-via phone bluetooth, 2-via gateway, 3-via NB-IoT. The default value is 1 and should call SDK method to add passcode first. If you use the method 2, you can call this api directly.
            """
            if isinstance(start_date, datetime):
                start_date = self.client._date_to_timestamp(start_date)

            if isinstance(end_date, datetime):
                end_date = self.client._date_to_timestamp(end_date)

            start_date = int(start_date)
            end_date = int(end_date)

            data = {
                "lockId": lock_id,
                "keyboardPwd": passcode,
                "keyboardPwdName": name[:20],
                "startDate": start_date,
                "endDate": end_date,
                "addType": add_type,
            }

            full_payload = self.client._prepare_api_payload(data)
            logging.getLogger(__name__).info(f"Creating passcode with payload: {data}")

            return await self.client.request(
                "POST", ENDPOINTS["keyboard_pwd_add"], data=full_payload
            )

        async def delete_passcode(self, lock_id: int, keyboard_pwd_id: int) -> dict:
            payload = self.client._prepare_api_payload(
                {"lockId": lock_id, "keyboardPwdId": keyboard_pwd_id}
            )
            return await self.client.request(
                "POST", ENDPOINTS["keyboard_pwd_delete"], data=payload
            )

    class _QR(__BaseType):
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
            return await self.client.request(
                "POST", QR_ENDPOINTS["delete"], data=payload
            )

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
            return await self.client.request(
                "POST", QR_ENDPOINTS["update"], data=payload
            )

        async def clear(self, lock_id: int) -> dict[str, Any]:
            await self._ensure_login()
            payload = self.client._prepare_api_payload({"lockId": lock_id})
            return await self.client.request(
                "POST", QR_ENDPOINTS["clear"], data=payload
            )


class LockControllerInterface(LockController):
    def Locks(self):
        return self._Locks(self)

    def Passcode(self):
        return self._Passcode(self)

    def QR(self):
        return self._QR(self)


# print(
#     asyncio.run(
#         LockControllerInterface(
#             client=TTLockClient(
#                 client_id="3c82d46d910f4fb8bb929af12bbcc68e",
#                 client_secret="1bca383acb15643d2b4dc20adbc8dbcd",
#                 username="nsq.studio@yandex.ru",
#                 password="nsq_studio141025",
#             )
#         ).Locks().get_all_locks()
#     )
# )
