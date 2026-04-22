from enum import IntEnum


class PasscodeType(IntEnum):
    ONE_TIME = 1
    PERMANENT = 2
    PERIOD = 3
    ERASE = 4
