"""Helper class to communicate with the Musicnode API."""
import logging

import requests


class MusicnodeApi:
    """Musicnode API Helper."""

    _LOGGER = logging.getLogger(__name__)

    def __init__(self, host: str, port: int) -> None:
        """Initialize."""
        self.host = host
        self.port = port
        self._LOGGER.info("MusicNodeAPI: %d:%d", self.host, self.port)

    def async_send_media_update(self, request: dict) -> bool:
        """Send the thing."""
        api_response = requests.put(
            f"{self.host}:{self.port}/Music/State", json=request, timeout=5000
        )
        return api_response.ok

    def async_send_screen_update(self, line1: str, line2: str) -> bool:
        """Send the thing."""
        mbody = {"Line1": line1, "Line2": line2}
        api_response = requests.put(
            f"{self.host}:{self.port}/Display/Message", json=mbody, timeout=5000
        )
        return api_response.ok
    
    def async_send_temporary_screen_update(self, line1: str, line2: str) -> bool:
        """Send the thing."""
        mbody = {"Line1": line1, "Line2": line2}
        api_response = requests.put(
            f"{self.host}:{self.port}/Display/TemporaryMessage", json=mbody, timeout=5000
        )
        return api_response.ok

    def async_healthcheck(self) -> int:
        """Check we can see the API."""
        api_response = requests.get(
            f"{self.host}:{self.port}/Util/Healthcheck", timeout=5000
        )
        return api_response.status_code

    def async_alarm(self) -> bool:
        """Trigger the Alarm"""
        api_response = requests.post(
            f"{self.host}:{self.port}/Alarm", timeout=5000
        )
        return api_response.ok
    
    def async_alert(self, message: str, bell: str) -> bool:
        """Read an alert message aloud"""
        mbody = {"bell": bell, "message": message}
        api_response = requests.put(
            f"{self.host}:{self.port}/Alert", json=mbody, timeout=5000
        )
        return api_response.ok
    
    def async_bell(self,  bell: str) -> bool:
        """Read an alert message aloud"""
        api_response = requests.put(
            f"{self.host}:{self.port}/Alert/Bell?bell={bell}", timeout=5000
        )
        return api_response.ok
    
