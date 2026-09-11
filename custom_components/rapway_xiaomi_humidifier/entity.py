"""Base entity for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODEL, DEFAULT_NAME


class XiaomiHumidifierEntity(CoordinatorEntity):
    """Base entity shared by all humidifier entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer="Xiaomi / Deerma",
            model=MODEL,
        )
