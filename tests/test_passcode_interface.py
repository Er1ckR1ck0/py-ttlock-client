from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from py_ttlock_client.interfaces.passcode import PasscodeInterface
from py_ttlock_client.schemas.passcode import (
    PasscodeAddResponse,
    PasscodeListResponse,
    PasscodeOperationResponse,
)
from py_ttlock_client.schemas.passcode import (
    PasscodeAddRequest,
    PasscodeGetRequest,
    PasscodeResponse,
)


def test_passcode_request_models_only_describe_business_fields():
    add_request = PasscodeAddRequest(
        lockId=1,
        keyboardPwd="123456",
        keyboardPwdName="Guest",
        startDate=1000,
        endDate=2000,
    )
    get_request = PasscodeGetRequest(
        lockId=1,
        keyboardPwdVersion=4,
        keyboardPwdType=2,
    )

    add_payload = add_request.model_dump(exclude_none=True)
    get_payload = get_request.model_dump(exclude_none=True)

    assert "clientId" not in add_payload
    assert "accessToken" not in add_payload
    assert "date" not in add_payload
    assert "keyboardPwdType" not in add_payload
    assert get_payload["keyboardPwdVersion"] == 4


@pytest.fixture
def mock_interface():
    client = MagicMock()
    client.access_token = "token"
    client._prepare_api_payload.side_effect = lambda payload: {
        "clientId": "client-id",
        "accessToken": "token",
        "date": 123,
        **payload,
    }
    client._date_to_timestamp.side_effect = lambda value: value
    client.request = AsyncMock()
    interface = SimpleNamespace(client=client, login=AsyncMock())
    return interface


@pytest.mark.asyncio
async def test_passcode_create(mock_interface):
    mock_interface.client.request.return_value = {"keyboardPwdId": 42}

    response = await PasscodeInterface(mock_interface).create(
        lock_id=1,
        passcode="123456",
        name="Guest",
        start_date=1000,
        end_date=2000,
    )

    assert isinstance(response, PasscodeAddResponse)
    method, endpoint = mock_interface.client.request.await_args.args
    payload = mock_interface.client.request.await_args.kwargs["data"]
    assert method == "POST"
    assert endpoint == "/v3/keyboardPwd/add"
    assert payload["lockId"] == 1
    assert payload["keyboardPwd"] == "123456"
    assert payload["keyboardPwdName"] == "Guest"


@pytest.mark.asyncio
async def test_passcode_get_and_list(mock_interface):
    iface = PasscodeInterface(mock_interface)

    mock_interface.client.request.return_value = {
        "keyboardPwd": "654321",
        "keyboardPwdId": 99,
    }
    get_response = await iface.get(
        lock_id=1,
        keyboard_pwd_version=4,
        keyboard_pwd_type=2,
        start_date=1000,
        end_date=2000,
    )
    assert isinstance(get_response, PasscodeResponse)

    mock_interface.client.request.return_value = {
        "list": [
            {
                "keyboardPwdId": 99,
                "lockId": 1,
                "keyboardPwd": "654321",
                "keyboardPwdType": 2,
            }
        ],
        "pageNo": 1,
        "pageSize": 20,
    }
    list_response = await iface.get_list(lock_id=1)
    assert isinstance(list_response, PasscodeListResponse)
    assert list_response.list_[0].keyboardPwdId == 99


@pytest.mark.asyncio
async def test_passcode_change_and_delete(mock_interface):
    mock_interface.client.request.return_value = {
        "errcode": 0,
        "errmsg": "none error message",
    }
    iface = PasscodeInterface(mock_interface)

    change_response = await iface.change(
        lock_id=1,
        keyboard_pwd_id=99,
        name="Updated",
        new_passcode="111111",
        start_date=1000,
        end_date=2000,
    )
    delete_response = await iface.delete(lock_id=1, keyboard_pwd_id=99)

    assert isinstance(change_response, PasscodeOperationResponse)
    assert isinstance(delete_response, PasscodeOperationResponse)
    change_call = mock_interface.client.request.await_args_list[0]
    delete_call = mock_interface.client.request.await_args_list[1]
    assert change_call.args == ("POST", "/v3/keyboardPwd/change")
    assert change_call.kwargs["data"]["newKeyboardPwd"] == "111111"
    assert delete_call.args == ("POST", "/v3/keyboardPwd/delete")
    assert delete_call.kwargs["data"]["keyboardPwdId"] == 99
