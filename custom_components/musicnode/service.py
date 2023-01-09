"""Musicnode Services."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, ServiceCall

from .const import (
    CONF_ENTITY_ID,
    CONF_FRIENDLY_ENTITY,
    CONF_NEW_ALBUM,
    CONF_NEW_ARTIST,
    CONF_NEW_STATE,
    CONF_NEW_TITLE,
    CONF_OLD_ALBUM,
    CONF_OLD_ARTIST,
    CONF_OLD_STATE,
    CONF_OLD_TITLE,
    CONF_BELL,
    CONF_MESSAGE,
    CONF_LINE_1,
    CONF_LINE_2,
    DOMAIN,
    SERVICES,
    SERVICE_ALARM,
    SERVICE_BELL,
    SERVICE_SPEAK,
    SERVICE_UPDATE,
    SERVICE_TEMP_MESSAGE
)

LOGGER = logging.getLogger(__name__)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Service handler setup."""

    async def update_service_handler(call: ServiceCall) -> None:
        """Handle service call."""

        api = hass.data[DOMAIN]["API"]

        request = {
            "entityId": call.data[CONF_ENTITY_ID],
            "friendlyName": call.data[CONF_FRIENDLY_ENTITY],
            "oldState": {
                "state": call.data[CONF_OLD_STATE],
                "mediaTitle": call.data[CONF_OLD_TITLE],
                "mediaArtist": call.data[CONF_OLD_ARTIST],
                "mediaAlbum": call.data[CONF_OLD_ALBUM],
            },
            "newState": {
                "state": call.data[CONF_NEW_STATE],
                "mediaTitle": call.data[CONF_NEW_TITLE],
                "mediaArtist": call.data[CONF_NEW_ARTIST],
                "mediaAlbum": call.data[CONF_NEW_ALBUM],
            },
        }

        await hass.async_add_executor_job(api.async_send_media_update, request)
        
    async def alarm_service_handler(call: ServiceCall) -> None:
        """Handle service call."""

        api = hass.data[DOMAIN]["API"]
        await hass.async_add_executor_job(api.async_alarm)
        
    async def speak_service_handler(call: ServiceCall) -> None:
        """Handle service call."""

        api = hass.data[DOMAIN]["API"]
        
        message = call.data[CONF_MESSAGE]
        bell = call.data[CONF_BELL]
        
        await hass.async_add_executor_job(api.async_alert, message, bell)        
    
    async def bell_service_handler(call: ServiceCall) -> None:
        """Handle service call."""

        api = hass.data[DOMAIN]["API"]
        
        bell = call.data[CONF_BELL]
        
        await hass.async_add_executor_job(api.async_bell, bell) 
        
    async def temp_msg_service_handler(call: ServiceCall) -> None:
        """Handle service call."""

        api = hass.data[DOMAIN]["API"]
        
        ln1 = call.data[CONF_LINE_1]
        ln2 = call.data[CONF_LINE_2]
        
        await hass.async_add_executor_job(api.async_send_temporary_screen_update, ln1, ln2)            
    

    # for service in SERVICES:
    hass.services.async_register(DOMAIN, SERVICE_UPDATE, update_service_handler)
    hass.services.async_register(DOMAIN, SERVICE_ALARM, alarm_service_handler)
    hass.services.async_register(DOMAIN, SERVICE_SPEAK, speak_service_handler)
    hass.services.async_register(DOMAIN, SERVICE_BELL, bell_service_handler)
    hass.services.async_register(DOMAIN, SERVICE_TEMP_MESSAGE, temp_msg_service_handler)
