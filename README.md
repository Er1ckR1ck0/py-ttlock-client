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

Configuration is loaded from `settings.py` automatically.

## Quick Start

```python
import asyncio

from lock import Lock
from settings import settings


async def main() -> None:
	client = Lock(
		client_id=settings.TTLOCK_CLIENT_ID,
		client_secret=settings.TTLOCK_CLIENT_SECRET,
		username=settings.TTLOCK_USERNAME,
		password=settings.TTLOCK_PASSWORD,
	)

	lock_list = await client.Lock.get_list(page=1, page_size=20)
	print(lock_list.total)

	if lock_list.list_:
		detail = await client.Lock.get_detail(lock_id=lock_list.list_[0].lockId)
		print(detail.lockAlias)


if __name__ == "__main__":
	asyncio.run(main())
```

Run the project example module:

```bash
uv run -m example
```

## API Overview

### Facade

Use `lock.Lock` as the main entry point:

- `client.Lock` -> lock management interface
- `client.Passcode` -> passcode management interface
- `client.QR` -> QR code management interface

### Lock Interface (`interfaces/lock.py`)

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

### Passcode Interface (`interfaces/passcode.py`)

- `create(lock_id, passcode, name=None, start_date, end_date, add_type=2)`
- `get(lock_id, keyboard_pwd_version, keyboard_pwd_type, name=None, start_date=None, end_date=None)`
- `get_list(lock_id, page=1, page_size=20)`
- `delete(lock_id, keyboard_pwd_id, delete_type=2)`
- `change(lock_id, keyboard_pwd_id, name=None, new_passcode=None, start_date=None, end_date=None, change_type=2)`
- `update(...)` (alias for `change`)

### QR Interface (`interfaces/qr_code.py`)

- `create(lock_id, qr_type, name=None, start_date=None, end_date=None, cyclic_config=None)`
- `get_list(lock_id, page=1, page_size=20, name=None)`
- `get(code_id)`
- `delete(lock_id, code_id)`
- `update(code_id, name=None, start_date=None, end_date=None, cyclic_config=None)`
- `clear(lock_id)`

## Provider Selection

The default provider is TTLock.

You can also use provider wrappers from `providers.py`:

- `TTLockClient`
- `ScienerClient`

Or pass explicit provider enum to `LockClient` / `Lock` using `LockProvider`.

## Enums

Available enums in `enums.py`:

- `PasscodeType`
- `LockState`
- `DeviceType`

## Error Handling

Provider/API errors are raised as `LockAPIError` from `modules/exceptions.py`.

```python
from modules.exceptions import LockAPIError

try:
	...
except LockAPIError as exc:
	print(exc.error_code, str(exc))
```

## Running Tests

```bash
uv run pytest
```

Current repository tests cover the main lock/passcode flows and model serialization constraints.

## Project Structure

```text
.
├── client.py
├── lock.py
├── settings.py
├── providers.py
├── enums.py
├── interfaces/
├── modules/
├── schemas/
├── tests/
├── example.py
└── pyproject.toml
```

## Notes

- The project uses a flat module layout (imports like `from lock import Lock`) when executed from repository root.
- If you integrate this as an installable package, keep import mode consistent across runtime and tests.
