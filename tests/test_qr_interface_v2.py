from unittest.mock import AsyncMock, MagicMock

import pytest

from ttlock_modules.qr_interface_v2 import ImprovedLockClient, QRControllerInterface
from ttlock_modules.schemas.qr import QRCodeCreateResponse, QRCodeData


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200
        self.text = str(payload)

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def build_client(**kwargs) -> ImprovedLockClient:
    http_client = MagicMock()
    http_client.request = AsyncMock()
    http_client.aclose = AsyncMock()
    defaults = {
        "client_id": "client-id",
        "client_secret": "client-secret",
        "username": "username",
        "password": "password",
        "access_token": "token",
        "http_client": http_client,
    }
    defaults.update(kwargs)
    return ImprovedLockClient(**defaults)


def test_prepare_api_payload_filters_none():
    client = build_client()

    payload = client._prepare_api_payload({"lockId": 1, "name": None})

    assert payload["clientId"] == "client-id"
    assert payload["accessToken"] == "token"
    assert payload["lockId"] == 1
    assert "name" not in payload


@pytest.mark.asyncio
async def test_request_uses_query_params_for_get():
    client = build_client()
    client.http_client.request.return_value = FakeResponse({"ok": True})

    response = await client.request("GET", "/v3/qrCode/getData", data={"qrCodeId": 7})

    assert response == {"ok": True}
    client.http_client.request.assert_awaited_once()
    _, url = client.http_client.request.await_args.args
    kwargs = client.http_client.request.await_args.kwargs
    assert url.endswith("/v3/qrCode/getData")
    assert kwargs["params"] == {"qrCodeId": 7}
    assert "data" not in kwargs


@pytest.mark.asyncio
async def test_qr_create_returns_typed_response():
    client = build_client()
    client.request = AsyncMock(
        return_value=QRCodeCreateResponse(
            qrCodeId=5, qrCodeNumber="001", link="https://qr"
        )
    )
    controller = QRControllerInterface(client)

    response = await controller.QR().create(
        lock_id=1,
        qr_type=1,
        name="Guest",
        start_date=1000,
        end_date=2000,
    )

    assert isinstance(response, QRCodeCreateResponse)
    method, endpoint = client.request.await_args.args
    kwargs = client.request.await_args.kwargs
    assert method == "POST"
    assert endpoint.endswith("/v3/qrCode/add")
    assert kwargs["data"]["lockId"] == 1
    assert kwargs["data"]["type"] == 1
    assert kwargs["data"]["name"] == "Guest"
    assert kwargs["data"]["startDate"] == 1000
    assert kwargs["data"]["endDate"] == 2000


@pytest.mark.asyncio
async def test_qr_get_parses_qrcode_data_alias():
    client = build_client()
    client.request = AsyncMock(
        return_value=QRCodeData(
            qrCodeId="7",
            qrCodeData="payload",
            lockAlias="Front door",
            type="1",
            qrCodeNumber="A1",
        )
    )
    controller = QRControllerInterface(client)

    response = await controller.QR().get(code_id=7)

    assert isinstance(response, QRCodeData)
    assert response.qrCodeContent == "payload"
    method, endpoint = client.request.await_args.args
    kwargs = client.request.await_args.kwargs
    assert method == "GET"
    assert endpoint.endswith("/v3/qrCode/getData")
    assert kwargs["params"]["qrCodeId"] == 7


@pytest.mark.asyncio
async def test_qr_delete_update_and_clear_use_expected_payloads():
    client = build_client()
    client.request = AsyncMock(
        return_value={"errcode": 0, "errmsg": "none error message"}
    )
    controller = QRControllerInterface(client)

    await controller.QR().delete(lock_id=3, code_id=9)
    await controller.QR().update(
        code_id=9,
        name="Updated",
        start_date=1000,
        end_date=2000,
        cyclic_config=[{"startTime": 480, "endTime": 1080, "weekDay": 1}],
    )
    await controller.QR().clear(lock_id=3)

    calls = client.request.await_args_list
    delete_call = calls[0]
    update_call = calls[1]
    clear_call = calls[2]

    assert delete_call.args == ("POST", "/v3/qrCode/delete")
    assert delete_call.kwargs["data"]["lockId"] == 3
    assert delete_call.kwargs["data"]["qrCodeId"] == 9

    assert update_call.args == ("POST", "/v3/qrCode/update")
    assert update_call.kwargs["data"]["qrCodeId"] == 9
    assert update_call.kwargs["data"]["name"] == "Updated"
    assert update_call.kwargs["data"]["cyclicConfig"] == [
        {"startTime": 480, "endTime": 1080, "weekDay": 1}
    ]

    assert clear_call.args == ("POST", "/v3/qrCode/clear")
    assert clear_call.kwargs["data"]["lockId"] == 3
