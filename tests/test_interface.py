import pytest
from unittest.mock import AsyncMock, MagicMock

from ttlock_modules.interface import LockControllerInterface
from ttlock_modules.client import LockClient
from ttlock_modules.schemas.qr import QRCodeData


@pytest.fixture
def mock_client():
    client = MagicMock(spec=LockClient)
    client.client_id = "test_client_id"
    client.client_secret = "test_client_secret"
    client.username = "test_username"
    client.password = "test_password"
    client.access_token = "fake_token"
    client._prepare_api_payload.return_value = {"fake": "payload"}
    client.request = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_interface_lock(mock_client):
    mock_client.request.return_value = {
        "list": [{"lockId": 1, "lockAlias": "Test Lock"}]
    }

    controller = LockControllerInterface(client=mock_client)
    locks = await controller.Locks().get_all_locks()

    assert len(locks) == 1
    assert locks[0]["lockAlias"] == "Test Lock"
    mock_client.request.assert_awaited_once()


@pytest.mark.asyncio
async def test_interface_passcode(mock_client):
    mock_client.request.return_value = {"keyboardPwdId": 123}
    mock_client._date_to_timestamp.side_effect = lambda x: x

    controller = LockControllerInterface(client=mock_client)
    res = await controller.Passcode().create_passcode(
        lock_id=1, name="Test", start_date=1000, end_date=2000, passcode="1234"
    )

    assert res["keyboardPwdId"] == 123
    mock_client.request.assert_awaited_once()


@pytest.mark.asyncio
async def test_interface_qr(mock_client):
    mock_client.request.return_value = {
        "qrCodeId": 1,
        "qrCodeData": "fake_data",
        "lockAlias": "Test",
        "type": 1,
        "qrCodeNumber": "001",
        "name": "fake",
        "startDate": 1000,
        "endDate": 2000,
        "status": 1,
    }

    controller = LockControllerInterface(client=mock_client)
    qr = await controller.QR().get(code_id=1)

    assert isinstance(qr, QRCodeData)
    mock_client.request.assert_awaited_once()
