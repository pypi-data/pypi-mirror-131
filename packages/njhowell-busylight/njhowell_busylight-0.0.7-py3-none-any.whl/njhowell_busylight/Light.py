from .Auth import Auth

class Light:
    """Class that represents a Light object in the ExampleHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a light object."""
        self.raw_data = raw_data
        self.auth = auth

    # Note: each property name maps the name in the returned data

    @property
    def id(self) -> int:
        """Return the ID of the light."""
        return 1

    @property
    def name(self) -> str:
        """Return the name of the light."""
        return "busylight"

    @property
    def is_on(self) -> bool:
        """Return if the light is on."""
        if(self.raw_data["status"] == "off"):
            return False
        else:
            return True
    
    @property
    def status(self) -> str:
        """Return the status of the light"""
        return self.raw_data["status"]

    async def async_control(self, is_on: bool):
        """Control the light."""
        if(is_on):
            url = "on"
        else:
            url = "off"        

        resp = await self.auth.request(
            "post", url
        )
        resp.raise_for_status()
        json = await resp.json()
        self.raw_data["is_on"] = is_on

    async def async_update(self):
        """Update the light data."""
        resp = await self.auth.request("get", f"status")
        resp.raise_for_status()
        self.raw_data = await resp.json()

    async def async_busy(self):
        """Set the light to busy"""
        resp = await self.auth.request("get", f"busy")
        resp.raise_for_status()

    async def async_available(self):
        """set the light to available"""
        resp = await self.auth.request("get", f"available")
        resp.raise_for_status()
        
    async def async_switch(self, red: int, green: int, blue: int):
        """Set light to specific colour"""
        resp = await self.auth.request("post", f"switch",json={"red": red, "green": green, "blue": blue})
        resp.raise_for_status()