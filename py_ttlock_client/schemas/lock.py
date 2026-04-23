from __future__ import annotations

from typing import Any

from pydantic import Field

from py_ttlock_client.schemas.base import TTLockSchema



class LockVersion(TTLockSchema):
    """Protocol / firmware version info returned as nested JSON in lock detail."""

    protocolType: int | None = None
    protocolVersion: int | None = None
    scene: int | None = None
    groupId: int | None = None
    orgId: int | None = None



class LockIdRequest(TTLockSchema):
    """Minimal request that only needs a lockId (lock/unlock/delete/freeze/…)."""

    lockId: int


class LockListRequest(TTLockSchema):
    """Parameters for /v3/lock/list."""

    lockAlias: str | None = None
    type: int | None = None  # 1=lock, 2=lift controller
    groupId: int | None = None
    pageNo: int = 1
    pageSize: int = 20


class LockRenameRequest(TTLockSchema):
    """Parameters for /v3/lock/rename."""

    lockId: int
    lockAlias: str


class LockTransferRequest(TTLockSchema):
    """Parameters for /v3/lock/transfer."""

    lockId: int
    receiverUsername: str


class LockAutoLockTimeRequest(TTLockSchema):
    """Parameters for /v3/lock/setAutoLockTime."""

    lockId: int
    seconds: int
    type: int = 2  # 1=via BLE, 2=via gateway


class LockBatteryUpdateRequest(TTLockSchema):
    """Parameters for /v3/lock/updateElectricQuantity."""

    lockId: int
    electricQuantity: int



class LockOperationResponse(TTLockSchema):
    """Standard operation response (lock/unlock/rename/delete/transfer/etc.)."""

    errcode: int = 0
    errmsg: str = ""
    description: str | None = None


class LockOpenStateResponse(TTLockSchema):
    """Response from /v3/lock/queryOpenState."""

    state: int  # 0=locked, 1=unlocked, 2=unknown


class LockDetail(TTLockSchema):
    """Full lock detail response from /v3/lock/detail."""

    lockId: int
    lockName: str | None = None
    lockAlias: str | None = None
    lockMac: str | None = None
    lockKey: str | None = None
    lockFlagPos: int | None = None
    adminPwd: str | None = None
    noKeyPwd: str | None = None
    deletePwd: str | None = None
    aesKeyStr: str | None = None
    lockVersion: LockVersion | dict[str, Any] | None = None
    keyboardPwdVersion: int | None = None
    electricQuantity: int | None = None
    specialValue: int | None = None
    timezoneRawOffset: int | None = None
    modelNum: str | None = None
    hardwareRevision: str | None = None
    firmwareRevision: str | None = None
    autoLockTime: int | None = None
    featureValue: str | None = None
    date: int | None = None


class LockListItem(TTLockSchema):
    """Single lock entry in the /v3/lock/list response."""

    lockId: int
    lockName: str | None = None
    lockAlias: str | None = None
    lockMac: str | None = None
    electricQuantity: int | None = None
    keyboardPwdVersion: int | None = None
    specialValue: int | None = None
    featureValue: str | None = None
    lockVersion: LockVersion | dict[str, Any] | None = None
    modelNum: str | None = None
    hardwareRevision: str | None = None
    firmwareRevision: str | None = None
    date: int | None = None


class LockListResponse(TTLockSchema):
    """Paginated response from /v3/lock/list."""

    list_: list[LockListItem] = Field(default_factory=list, alias="list")
    pageNo: int | None = None
    pageSize: int | None = None
    pages: int | None = None
    total: int | None = None
