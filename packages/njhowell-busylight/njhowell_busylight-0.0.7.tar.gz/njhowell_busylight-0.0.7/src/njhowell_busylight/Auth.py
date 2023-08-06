from aiohttp import ClientSession, ClientResponse

class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str):
        """Initialize the auth."""
        self.host = host
        self.websession = websession

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""

        return await self.websession.request(
            method, f"{self.host}/{path}", **kwargs,
        )