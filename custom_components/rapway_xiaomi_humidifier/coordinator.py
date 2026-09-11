"""Coordinator for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from datetime import timedelta
from functools import partial
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from miio import AirHumidifierJsqs, DeviceException

from .const import (
    CONF_HOST,
    CONF_TOKEN,
    DOMAIN,
    MODEL,
    UPDATE_INTERVAL_SECONDS,
)

_LOGGER = logging.getLogger(__name__)


class XiaomiHumidifierCoordinator(DataUpdateCoordinator):
    """Coordinate one local status request for all entities."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.host = entry.data[CONF_HOST]
        self.token = entry.data[CONF_TOKEN]
        self.device = AirHumidifierJsqs(self.host, self.token, model=MODEL)

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(self.device.status)
        except DeviceException as err:
            raise UpdateFailed(f"Cannot communicate with humidifier: {err}") from err

    async def async_command(self, method, *args):
        """Run a blocking miio command and refresh state afterwards."""
        try:
            result = await self.hass.async_add_executor_job(
                partial(method, *args)
            )
        except DeviceException as err:
            raise UpdateFailed(f"Command failed: {err}") from err

        await self.async_request_refresh()
        return result
