# py-ttlock-client

Async Python client for TTLock/Sciener APIs with typed Pydantic schemas and high-level interface wrappers for locks, passcodes, and QR codes.

[Русская версия](README.ru.md)

## Features

- Async HTTP client powered by `httpx`.
- Environment-based configuration via `pydantic-settings`.
- Typed request/response schemas via `pydantic`.
- High-level facade object (`Lock`) with grouped interfaces:
  - `Lock` operations (list/detail/state/control).
  - `Passcode` operations (create/get/list/change/delete).
  - `QR` operations (create/get/list/update/delete/clear).
- Provider support for both TTLock and Sciener base URLs.
- Test suite with `pytest` + `pytest-asyncio`.

## Requirements

- Python `>= 3.13`
- `uv` (recommended) or a standard Python virtual environment setup

## Installation

```bash
pip install py-ttlock-client
```

Or for development:

```bash
git clone https://github.com/er1ckr1ck0/py-ttlock-client.git
cd py-ttlock-client
uv sync
```

## Configuration

Create a `.env` file in the project root:

```dotenv
TTLOCK_CLIENT_ID=your_client_id
TTLOCK_CLIENT_SECRET=your_client_secret
TTLOCK_USERNAME=your_username
TTLOCK_PASSWORD=your_password
```

Configuration is loaded automatically via `pydantic-settings`.

## Quick Start

```python
import asyncio

from py_ttlock_client import Lock


async def main() -> None:
	client = Lock(
		client_id="your_client_id",
		client_secret="your_client_secret",
		username="your_username",
		password="your_password",
	)

	lock_list = await client.Lock.get_list(page=1, page_size=20)
	print(lock_list.total)

	if lock_list.list_:
		detail = await client.Lock.get_detail(lock_id=lock_list.list_[0].lockId)
		print(detail.lockAlias)


if __name__ == "__main__":
	asyncio.run(main())
```

## API Overview

### Facade

Use `py_ttlock_client.Lock` as the main entry point:

- `client.Lock` -> lock management interface
- `client.Passcode` -> passcode management interface
- `client.QR` -> QR code management interface

### Lock Interface

- `get_list(page=1, page_size=20, lock_alias=None, device_type=None, group_id=None)`
- `get_detail(lock_id)`
- `lock(lock_id)`
- `unlock(lock_id)`
- `rename(lock_id, alias)`
- `delete(lock_id)`
- `transfer(lock_id, receiver_username)`
- `query_open_state(lock_id)`
- `set_auto_lock_time(lock_id, seconds, via_gateway=True)`
- `update_battery(lock_id, electric_quantity)`
- `freeze(lock_id)`
- `unfreeze(lock_id)`

### Passcode Interface

- `create(lock_id, passcode, name=None, start_date, end_date, add_type=2)`
- `get(lock_id, keyboard_pwd_version, keyboard_pwd_type, name=None, start_date=None, end_date=None)`
- `get_list(lock_id, page=1, page_size=20)`
- `delete(lock_id, keyboard_pwd_id, delete_type=2)`
- `change(lock_id, keyboard_pwd_id, name=None, new_passcode=None, start_date=None, end_date=None, change_type=2)`
- `update(...)` (alias for `change`)

### QR Interface

- `create(lock_id, qr_type, name=None, start_date=None, end_date=None, cyclic_config=None)`
- `get_list(lock_id, page=1, page_size=20, name=None)`
- `get(code_id)`
- `delete(lock_id, code_id)`
- `update(code_id, name=None, start_date=None, end_date=None, cyclic_config=None)`
- `clear(lock_id)`

## Provider Selection

The default provider is TTLock.

You can also use provider wrappers:

```python
from py_ttlock_client import TTLockClient, ScienerClient
```

Or pass explicit provider enum to `LockClient` / `Lock` using `LockProvider`.

## Enums

Available enums:

```python
from py_ttlock_client import PasscodeType, LockState, DeviceType
```

- `PasscodeType` — ONE_TIME, PERMANENT, PERIOD, ERASE
- `LockState` — LOCKED, UNLOCKED, UNKNOWN
- `DeviceType` — LOCK, LIFT_CONTROLLER

## Error Handling

```python
from py_ttlock_client import LockAPIError

try:
	...
except LockAPIError as exc:
	print(exc.error_code, str(exc))
```

## Running Tests

```bash
uv run pytest
```

## Project Structure

```text
py_ttlock_client/
├── __init__.py
├── client.py
├── lock.py
├── settings.py
├── providers.py
├── enums.py
├── modules/
│   ├── constants.py
│   ├── exceptions.py
│   └── interface.py
├── interfaces/
│   ├── base_interface.py
│   ├── lock.py
│   ├── passcode.py
│   └── qr_code.py
└── schemas/
    ├── base.py
    ├── lock.py
    ├── passcode.py
    └── qr.py
```

## License

MIT
