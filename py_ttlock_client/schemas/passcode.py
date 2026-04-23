from pydantic import Field

from py_ttlock_client.schemas.base import TTLockSchema


class PasscodeRequestBase(TTLockSchema):
    lockId: int
    keyboardPwdName: str | None = None


class PasscodeTimedRequest(PasscodeRequestBase):
    startDate: int | None = None
    endDate: int | None = None


class PasscodeGetRequest(PasscodeTimedRequest):
    keyboardPwdVersion: int
    keyboardPwdType: int


class PasscodeAddRequest(PasscodeTimedRequest):
    keyboardPwd: str | int
    startDate: int
    endDate: int
    addType: int = 2


class PasscodeDeleteRequest(TTLockSchema):
    lockId: int
    keyboardPwdId: int
    deleteType: int = 2


class PasscodeListRequest(TTLockSchema):
    lockId: int
    pageNo: int
    pageSize: int


class PasscodeChangeRequest(TTLockSchema):
    lockId: int
    keyboardPwdId: int
    keyboardPwdName: str | None = None
    newKeyboardPwd: str | None = None
    startDate: int | None = None
    endDate: int | None = None
    changeType: int = 2


class PasscodeResponseBase(TTLockSchema):
    keyboardPwdId: int


class PasscodeResponse(PasscodeResponseBase):
    keyboardPwd: str


class PasscodeOperationResponse(TTLockSchema):
    errcode: int
    errmsg: str
    description: str | None = None


class PasscodeListItem(TTLockSchema):
    keyboardPwdId: int
    lockId: int
    keyboardPwd: str | None = None
    keyboardPwdName: str | None = None
    keyboardPwdVersion: int | None = None
    keyboardPwdType: int | None = None
    startDate: int | None = None
    endDate: int | None = None
    sendDate: int | None = None
    isCustom: int | None = None
    status: int | None = None
    senderUsername: str | None = None


class PasscodeListResponse(TTLockSchema):
    list_: list[PasscodeListItem] = Field(default_factory=list, alias="list")
    pageNo: int | None = None
    pageSize: int | None = None
    pages: int | None = None
    total: int | None = None


PasscodeAddResponse = PasscodeResponseBase
