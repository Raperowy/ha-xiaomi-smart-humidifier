"""Binary sensor platform for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from .entity import XiaomiHumidifierEntity


@dataclass(frozen=True)
class BinaryDescription:
    key: str
    name: str
    device_class: BinarySensorDeviceClass
    value_fn: Callable


BINARY_SENSORS = (
    BinaryDescription(
        "no_water",
        "No water",
        BinarySensorDeviceClass.PROBLEM,
        lambda s: bool(s.water_shortage_fault),
    ),
    BinaryDescription(
        "tank_detached",
        "Water tank detached",
        BinarySensorDeviceClass.PROBLEM,
        lambda s: bool(s.tank_filed),
    ),
)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        XiaomiHumidifierBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class XiaomiHumidifierBinarySensor(XiaomiHumidifierEntity, BinarySensorEntity):
    def __init__(self, coordinator, description: BinaryDescription) -> None:
        super().__init__(coordinator, description.key)
        self.description = description
        self._attr_name = description.name
        self._attr_device_class = description.device_class

    @property
    def is_on(self):
        return self.description.value_fn(self.coordinator.data)
