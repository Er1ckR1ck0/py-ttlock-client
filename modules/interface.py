from client import LockClient
from modules.constants import ENDPOINTS


class LockController:
    """Controller responsible for authentication against lock provider APIs."""

    def __init__(self, client: LockClient):
        """Initialize controller with a configured client and validate credentials."""
        self.client = client
        if not all(
            [
                self.client.client_id,
                self.client.client_secret,
                self.client.username,
                self.client.password,
            ]
        ):
            raise ValueError(
                "Missing credentials for login (client_id, client_secret, username, password)"
            )

    async def login(self) -> None:
        """Authenticate the client and persist access_token on the client object."""
        if self.client.__dict__.get("access_token") is not None:
            return

        data = {
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "username": self.client.username,
            "password": self.client.password,
            "redirect_uri": "http://localhost:8000",
            "grant_type": "password",
        }

        response = await self.client.request(
            "POST", ENDPOINTS["oauth_token"], data=data
        )
        self.client.access_token = response.get("access_token")
