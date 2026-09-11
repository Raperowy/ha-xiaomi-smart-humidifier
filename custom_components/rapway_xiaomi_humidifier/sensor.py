"""Sensor platform for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfTemperature

from .entity import XiaomiHumidifierEntity


@dataclass(frozen=True)
class SensorDescription:
    key: str
    name: str
    device_class: SensorDeviceClass | None
    native_unit: str | None
    value_fn: Callable


SENSORS = (
    SensorDescription(
        "humidity",
        "Humidity",
        SensorDeviceClass.HUMIDITY,
        PERCENTAGE,
        lambda s: s.relative_humidity,
    ),
    SensorDescription(
        "temperature",
        "Temperature",
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        lambda s: s.temperature,
    ),
)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        XiaomiHumidifierSensor(coordinator, description)
        for description in SENSORS
    )


class XiaomiHumidifierSensor(XiaomiHumidifierEntity, SensorEntity):
    def __init__(self, coordinator, description: SensorDescription) -> None:
        super().__init__(coordinator, description.key)
        self.description = description
        self._attr_name = description.name
        self._attr_device_class = description.device_class
        self._attr_native_unit_of_measurement = description.native_unit

    @property
    def native_value(self):
        return self.description.value_fn(self.coordinator.data)
