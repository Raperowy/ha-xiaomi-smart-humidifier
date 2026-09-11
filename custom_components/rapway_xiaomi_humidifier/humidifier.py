"""Humidifier platform for Xiaomi Smart Humidifier."""

from __future__ import annotations

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
)

from miio.integrations.humidifier.deerma.airhumidifier_jsqs import OperationMode

from .entity import XiaomiHumidifierEntity

MODE_TO_OPERATION = {
    "Low": OperationMode.Low,
    "Mid": OperationMode.Mid,
    "High": OperationMode.High,
    "Auto": OperationMode.Auto,
}


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up the humidifier entity."""
    async_add_entities([XiaomiSmartHumidifier(entry.runtime_data)])


class XiaomiSmartHumidifier(XiaomiHumidifierEntity, HumidifierEntity):
    """Main Xiaomi Smart Humidifier control."""

    _attr_name = None
    _attr_icon = "mdi:air-humidifier"
    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER
    _attr_available_modes = list(MODE_TO_OPERATION)
    _attr_min_humidity = 40
    _attr_max_humidity = 80
    _attr_target_humidity_step = 1
    _attr_supported_features = HumidifierEntityFeature.MODES

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "humidifier")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_on

    @property
    def current_humidity(self) -> float | None:
        return self.coordinator.data.relative_humidity

    @property
    def target_humidity(self) -> float | None:
        return self.coordinator.data.target_humidity

    @property
    def mode(self) -> str | None:
        mode = self.coordinator.data.mode
        return mode.name if mode is not None else None

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_command(self.coordinator.device.on)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_command(self.coordinator.device.off)

    async def async_set_humidity(self, humidity: int) -> None:
        await self.coordinator.async_command(
            self.coordinator.device.set_target_humidity,
            int(humidity),
        )

    async def async_set_mode(self, mode: str) -> None:
        await self.coordinator.async_command(
            self.coordinator.device.set_mode,
            MODE_TO_OPERATION[mode],
        )
