from enum import IntEnum


class PasscodeType(IntEnum):
    ONE_TIME = 1
    PERMANENT = 2
    PERIOD = 3
    ERASE = 4


class LockState(IntEnum):
    LOCKED = 0
    UNLOCKED = 1
    UNKNOWN = 2


class DeviceType(IntEnum):
    LOCK = 1
    LIFT_CONTROLLER = 2

