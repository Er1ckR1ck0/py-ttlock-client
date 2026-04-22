from typing import Optional

from pydantic import AliasChoices, Field

from schemas.base import BaseLockCreate, TTLockSchema


class CyclicConfig(TTLockSchema):
    startTime: int
    endTime: int
    weekDay: int


class QRCodeGetRequest(BaseLockCreate):
    qrCodeId: int


class QRCodeCreateRequest(BaseLockCreate):
    lockId: int
    type: int
    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    cyclicConfig: list[CyclicConfig] | None = None


class QRCodeListRequest(BaseLockCreate):
    lockId: int
    pageNo: int
    pageSize: int
    name: Optional[str] = None


class QRCodeListItem(TTLockSchema):
    qrCodeId: int
    lockId: int
    type_: int = Field(alias="type")
    qrCodeNumber: str | int
    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    refreshTime: Optional[str] = None
    cyclicConfig: list[CyclicConfig] = Field(default_factory=list)
    createDate: Optional[str] = None
    status: Optional[str] = None
    creator: Optional[str] = None
    link: str | Optional[str] = None
    qrCodeVersion: Optional[str] = None


class QRCodeData(TTLockSchema):
    qrCodeId: Optional[str] = None
    lockId: Optional[str] = None
    lockAlias: Optional[str] = None
    type_: Optional[str] = Field(default=None, alias="type")
    qrCodeNumber: str | Optional[str] = None
    qrCodeContent: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("qrCodeContent", "qrCodeData"),
        serialization_alias="qrCodeContent",
    )
    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    refreshTime: Optional[str] = None
    cyclicConfig: list[CyclicConfig] = Field(default_factory=list)
    status: Optional[str] = None
    creator: Optional[str] = None
    link: str | Optional[str] = None
    qrCodeVersion: Optional[str] = None


class QRCodeCreateResponse(TTLockSchema):
    qrCodeId: int
    qrCodeNumber: str | int
    link: str | Optional[str] = None


class QRCodeListResponse(TTLockSchema):
    list_: list[QRCodeListItem] = Field(default_factory=list, alias="list")
    pageNo: Optional[str] = None
    pageSize: Optional[str] = None
    pages: Optional[str] = None
    total: Optional[str] = None


class QRCodeDeleteRequest(TTLockSchema):
    lockId: int
    qrCodeId: int
    deleteType: int = 2


class QRCodeUpdateRequest(TTLockSchema):
    qrCodeId: int
    name: Optional[str] = None
    startDate: Optional[int] = None
    endDate: Optional[int] = None
    refreshTime: Optional[int] = None
    cyclicConfig: Optional[CyclicConfig] = None
    type_: int = Field(default=None, alias="type")
    changeType: int = 2


class QRCodeClearRequest(TTLockSchema):
    lockId: Optional[str] = None
    type_: int = Field(default=2, alias="type")


QRCodeItemResponse = QRCodeListItem
QRCodeRequest = QRCodeGetRequest
QRCodeResponse = QRCodeCreateResponse
QRCodeRequestCreate = QRCodeListRequest
