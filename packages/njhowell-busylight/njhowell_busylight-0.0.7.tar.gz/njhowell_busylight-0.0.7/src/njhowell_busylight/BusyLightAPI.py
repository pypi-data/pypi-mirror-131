from .Auth import Auth
from .Light import Light



class BusyLightAPI:
    """Class to communicate with the ExampleHub API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_light(self) -> Light:
        """Return the light."""
        resp = await self.auth.request("get", f"status")
        resp.raise_for_status()
        return Light(await resp.json(), self.auth)