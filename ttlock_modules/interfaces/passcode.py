from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from ttlock_modules.constants import ENDPOINTS
from ttlock_modules.interfaces.base_interface import BaseInterface
from ttlock_modules.schemas.passcode import (
    PasscodeAddRequest,
    PasscodeAddResponse,
    PasscodeChangeRequest,
    PasscodeDeleteRequest,
    PasscodeGetRequest,
    PasscodeListResponse,
    PasscodeListRequest,
    PasscodeOperationResponse,
    PasscodeResponse,
)

PASSCODE_ENDPOINTS = {
    "get": ENDPOINTS["keyboard_pwd_get"],
    "add": ENDPOINTS["keyboard_pwd_add"],
    "list": "/v3/lock/listKeyboardPwd",
    "delete": ENDPOINTS["keyboard_pwd_delete"],
    "change": "/v3/keyboardPwd/change",
}


class PasscodeInterface(BaseInterface):
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

    async def create(
        self,
        lock_id: int,
        passcode: str | int,
        *,
        name: str | None = None,
        start_date: int | datetime | str,
        end_date: int | datetime | str,
        add_type: int = 2,
    ) -> PasscodeAddResponse:
        await self._ensure_login()
        payload = self._prepare_payload(
            PasscodeAddRequest(
                lockId=lock_id,
                keyboardPwd=str(passcode),
                keyboardPwdName=name,
                startDate=self._normalize_date(start_date),
                endDate=self._normalize_date(end_date),
                addType=add_type,
            )
        )
        return await self._request(
            "POST",
            PASSCODE_ENDPOINTS["add"],
            payload,
            PasscodeAddResponse,
        )

    async def get(
        self,
        lock_id: int,
        keyboard_pwd_version: int,
        keyboard_pwd_type: int,
        *,
        name: str | None = None,
        start_date: int | datetime | str | None = None,
        end_date: int | datetime | str | None = None,
    ) -> PasscodeResponse:
        await self._ensure_login()
        payload = self._prepare_payload(
            PasscodeGetRequest(
                lockId=lock_id,
                keyboardPwdVersion=keyboard_pwd_version,
                keyboardPwdType=keyboard_pwd_type,
                keyboardPwdName=name,
                startDate=self._normalize_date(start_date),
                endDate=self._normalize_date(end_date),
            )
        )
        return await self._request(
            "POST",
            PASSCODE_ENDPOINTS["get"],
            payload,
            PasscodeResponse,
        )

    async def get_list(
        self,
        lock_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> PasscodeListResponse:
        await self._ensure_login()
        payload = self._prepare_payload(
            PasscodeListRequest(
                lockId=lock_id,
                pageNo=page,
                pageSize=page_size,
            )
        )
        return await self._request(
            "POST",
            PASSCODE_ENDPOINTS["list"],
            payload,
            PasscodeListResponse,
        )

    async def delete(
        self,
        lock_id: int,
        keyboard_pwd_id: int,
        *,
        delete_type: int = 2,
    ) -> PasscodeOperationResponse:
        await self._ensure_login()
        payload = self._prepare_payload(
            PasscodeDeleteRequest(
                lockId=lock_id,
                keyboardPwdId=keyboard_pwd_id,
                deleteType=delete_type,
            )
        )
        return await self._request(
            "POST",
            PASSCODE_ENDPOINTS["delete"],
            payload,
            PasscodeOperationResponse,
        )

    async def change(
        self,
        lock_id: int,
        keyboard_pwd_id: int,
        *,
        name: str | None = None,
        new_passcode: str | int | None = None,
        start_date: int | datetime | str | None = None,
        end_date: int | datetime | str | None = None,
        change_type: int = 2,
    ) -> PasscodeOperationResponse:
        await self._ensure_login()
        payload = self._prepare_payload(
            PasscodeChangeRequest(
                lockId=lock_id,
                keyboardPwdId=keyboard_pwd_id,
                keyboardPwdName=name,
                newKeyboardPwd=(
                    str(new_passcode) if new_passcode is not None else None
                ),
                startDate=self._normalize_date(start_date),
                endDate=self._normalize_date(end_date),
                changeType=change_type,
            )
        )
        return await self._request(
            "POST",
            PASSCODE_ENDPOINTS["change"],
            payload,
            PasscodeOperationResponse,
        )

    async def update(
        self,
        lock_id: int,
        keyboard_pwd_id: int,
        *,
        name: str | None = None,
        new_passcode: str | int | None = None,
        start_date: int | datetime | str | None = None,
        end_date: int | datetime | str | None = None,
        change_type: int = 2,
    ) -> PasscodeOperationResponse:
        return await self.change(
            lock_id=lock_id,
            keyboard_pwd_id=keyboard_pwd_id,
            name=name,
            new_passcode=new_passcode,
            start_date=start_date,
            end_date=end_date,
            change_type=change_type,
        )
