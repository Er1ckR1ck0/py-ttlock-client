from enum import StrEnum


class LockProvider(StrEnum):
    TTLOCK = "ttlock"
    SCIENER = "sciener"


TTLOCK_API_BASE_URL = "https://api.ttlock.com"
SCIENER_API_BASE_URL = "https://api.sciener.com"

PROVIDER_BASE_URLS = {
    LockProvider.TTLOCK: TTLOCK_API_BASE_URL,
    LockProvider.SCIENER: SCIENER_API_BASE_URL,
}

ENDPOINTS = {
    "oauth_token": "/oauth2/token",
    
    "lock_list": "/v3/lock/list",
    "lock_detail": "/v3/lock/detail",
    "lock_lock": "/v3/lock/lock",
    "lock_unlock": "/v3/lock/unlock",
    "lock_rename": "/v3/lock/rename",
    "lock_delete": "/v3/lock/delete",
    "lock_transfer": "/v3/lock/transfer",
    "lock_query_open_state": "/v3/lock/queryOpenState",
    "lock_set_auto_lock_time": "/v3/lock/setAutoLockTime",
    "lock_update_electric_quantity": "/v3/lock/updateElectricQuantity",
    "lock_freeze": "/v3/lock/freeze",
    "lock_unfreeze": "/v3/lock/unfreeze",
    
    "keyboard_pwd_get": "/v3/keyboardPwd/get",
    "keyboard_pwd_add": "/v3/keyboardPwd/add",
    "keyboard_pwd_delete": "/v3/keyboardPwd/delete",
    "keyboard_pwd_change": "/v3/keyboardPwd/change",
    "keyboard_pwd_list": "/v3/lock/listKeyboardPwd",
    
    "qrcode_add": "/v3/qrCode/add",
    "qrcode_get_all": "/v3/qrCode/getAll",
    "qrcode_get_one": "/v3/qrCode/get",
    "qrcode_delete": "/v3/qrCode/delete",
    "qrcode_update": "/v3/qrCode/update",
    "qrcode_clear": "/v3/qrCode/clear",
}
