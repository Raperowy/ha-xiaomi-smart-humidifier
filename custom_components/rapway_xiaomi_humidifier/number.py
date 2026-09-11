"""Number platform for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE

from .entity import XiaomiHumidifierEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([XiaomiHumidifierTargetHumidity(entry.runtime_data)])


class XiaomiHumidifierTargetHumidity(XiaomiHumidifierEntity, NumberEntity):
    _attr_name = "Target humidity"
    _attr_icon = "mdi:water-percent"
    _attr_native_min_value = 40
    _attr_native_max_value = 80
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "target_humidity")

    @property
    def native_value(self):
        return self.coordinator.data.target_humidity

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_command(
            self.coordinator.device.set_target_humidity,
            int(value),
        )
