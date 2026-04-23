import pytest
from unittest.mock import AsyncMock

from py_ttlock_client.lock import Lock
from py_ttlock_client.schemas.qr import QRCodeData


@pytest.fixture
def mock_client():
    client = Lock(
        client_id="test_client_id",
        client_secret="test_client_secret",
        username="test_username",
        password="test_password",
    )
    client.access_token = "token"
    client._date_to_timestamp = lambda value: value
    client.request = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_interface_lock(mock_client):
    mock_client.request.return_value = {
        "list": [{"lockId": 1, "lockAlias": "Test Lock"}],
        "pageNo": 1,
        "pageSize": 20,
    }

    locks = await mock_client.Lock.get_list()

    assert len(locks.list_) == 1
    assert locks.list_[0].lockAlias == "Test Lock"
    mock_client.request.assert_awaited_once()


@pytest.mark.asyncio
async def test_interface_passcode(mock_client):
    mock_client.request.return_value = {"keyboardPwdId": 123}

    res = await mock_client.Passcode.create(
        lock_id=1,
        name="Test",
        start_date=1000,
        end_date=2000,
        passcode="1234",
    )

    assert res.keyboardPwdId == 123
    mock_client.request.assert_awaited_once()


@pytest.mark.asyncio
async def test_interface_qr(mock_client):
    mock_client.request.return_value = QRCodeData(
        qrCodeId="1",
        qrCodeData="fake_data",
        lockAlias="Test",
        type="1",
        qrCodeNumber="001",
    )

    qr = await mock_client.QR.get(code_id=1)

    assert isinstance(qr, QRCodeData)
    mock_client.request.assert_awaited_once()
