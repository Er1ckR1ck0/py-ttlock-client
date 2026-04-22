from client import LockClient

from interfaces.lock import LockInterface
from interfaces.passcode import PasscodeInterface
from interfaces.qr_code import QRInterface

from modules.constants import ENDPOINTS, LockProvider


class Lock(LockClient):
    """High-level facade exposing lock, passcode, and QR interfaces."""

    def __init__(self, provider = LockProvider.TTLOCK, client_id = None, client_secret = None, username = None, password = None):
        """Initialize provider client and bind feature-specific interfaces."""
        super().__init__(provider, client_id, client_secret, username, password)

        # Interface classes expect an object with a `.client` attribute.
        self.client = self
        
        self.Lock = LockInterface(self)
        self.QR = QRInterface(self)
        self.Passcode = PasscodeInterface(self)

    async def login(self) -> None:
        """Authenticate with OAuth password grant and cache access token."""
        if getattr(self, "access_token", None):
            return

        if not all([self.client_id, self.client_secret, self.username, self.password]):
            raise ValueError(
                "Missing credentials for login (client_id, client_secret, username, password)"
            )

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
            "redirect_uri": "http://localhost:8000",
            "grant_type": "password",
        }
        response = await self.request("POST", ENDPOINTS["oauth_token"], data=data)
        self.access_token = response.get("access_token")
    
    
            