# py-ttlock-client

Асинхронный Python-клиент для API TTLock/Sciener с типизированными Pydantic-схемами и высокоуровневыми интерфейсами для замков, кодов и QR.

[English version](README.md)

## Возможности

- Асинхронный HTTP-клиент на базе `httpx`.
- Конфигурация через переменные окружения с `pydantic-settings`.
- Типизированные запросы и ответы через `pydantic`.
- Фасадный объект `Lock` с группировкой операций:
  - операции с замками (`Lock`),
  - операции с кодами (`Passcode`),
  - операции с QR (`QR`).
- Поддержка провайдеров TTLock и Sciener.
- Набор тестов на `pytest` + `pytest-asyncio`.

## Требования

- Python `>= 3.13`
- `uv` (рекомендуется) или любой стандартный способ работы с venv

## Установка

```bash
uv sync
```

## Настройка

Создайте файл `.env` в корне проекта:

```dotenv
TTLOCK_CLIENT_ID=your_client_id
TTLOCK_CLIENT_SECRET=your_client_secret
TTLOCK_USERNAME=your_username
TTLOCK_PASSWORD=your_password
```

Настройки автоматически загружаются из `settings.py`.

## Быстрый старт

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

Запуск примера из репозитория:

```bash
uv run -m example
```

## Обзор API

### Фасад

`lock.Lock` является основной точкой входа:

- `client.Lock` -> интерфейс управления замком
- `client.Passcode` -> интерфейс управления кодами
- `client.QR` -> интерфейс управления QR

### Интерфейс замков (`interfaces/lock.py`)

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

### Интерфейс кодов (`interfaces/passcode.py`)

- `create(lock_id, passcode, name=None, start_date, end_date, add_type=2)`
- `get(lock_id, keyboard_pwd_version, keyboard_pwd_type, name=None, start_date=None, end_date=None)`
- `get_list(lock_id, page=1, page_size=20)`
- `delete(lock_id, keyboard_pwd_id, delete_type=2)`
- `change(lock_id, keyboard_pwd_id, name=None, new_passcode=None, start_date=None, end_date=None, change_type=2)`
- `update(...)` (алиас для `change`)

### Интерфейс QR (`interfaces/qr_code.py`)

- `create(lock_id, qr_type, name=None, start_date=None, end_date=None, cyclic_config=None)`
- `get_list(lock_id, page=1, page_size=20, name=None)`
- `get(code_id)`
- `delete(lock_id, code_id)`
- `update(code_id, name=None, start_date=None, end_date=None, cyclic_config=None)`
- `clear(lock_id)`

## Выбор провайдера

По умолчанию используется TTLock.

Также доступны обертки из `providers.py`:

- `TTLockClient`
- `ScienerClient`

Либо можно явно передать провайдера через `LockProvider` в `LockClient` / `Lock`.

## Перечисления

В `enums.py` доступны:

- `PasscodeType`
- `LockState`
- `DeviceType`

## Обработка ошибок

Ошибки API поднимаются как `LockAPIError` из `modules/exceptions.py`.

```python
from modules.exceptions import LockAPIError

try:
    ...
except LockAPIError as exc:
    print(exc.error_code, str(exc))
```

## Запуск тестов

```bash
uv run pytest
```

Текущий набор тестов покрывает базовые сценарии lock/passcode и сериализацию моделей.

## Структура проекта

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

## Примечания

- В проекте используется плоская структура модулей (например, `from lock import Lock`) при запуске из корня репозитория.
- При упаковке проекта как installable package важно поддерживать единый режим импортов между runtime и тестами.