class LockError(Exception):
    pass


class LockAPIError(LockError):
    def __init__(self, message: str, error_code: int | None = None):
        self.error_code = error_code
        super().__init__(f"{message} (Code: {error_code})" if error_code else message)


TTLockError = LockError
TTLockAPIError = LockAPIError

LockListNotExist = LockAPIError(message="Not Lock List", error_code=404)
