"""Fan platform for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from homeassistant.components.fan import FanEntity, FanEntityFeature

from miio.integrations.humidifier.deerma.airhumidifier_jsqs import OperationMode

from .entity import XiaomiHumidifierEntity

PRESET_TO_MODE = {
    "Low": OperationMode.Low,
    "Mid": OperationMode.Mid,
    "High": OperationMode.High,
    "Auto": OperationMode.Auto,
}


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up fan entity."""
    async_add_entities([XiaomiHumidifierFan(entry.runtime_data)])


class XiaomiHumidifierFan(XiaomiHumidifierEntity, FanEntity):
    """Main humidifier control."""

    _attr_name = None
    _attr_icon = "mdi:air-humidifier"
    _attr_preset_modes = list(PRESET_TO_MODE)
    _attr_supported_features = (
        FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.PRESET_MODE
    )

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "fan")

    @property
    def is_on(self):
        return self.coordinator.data.is_on

    @property
    def preset_mode(self):
        mode = self.coordinator.data.mode
        return mode.name if mode is not None else None

    async def async_turn_on(self, percentage=None, preset_mode=None, **kwargs) -> None:
        if preset_mode is not None:
            await self.coordinator.async_command(
                self.coordinator.device.set_mode,
                PRESET_TO_MODE[preset_mode],
            )
        else:
            await self.coordinator.async_command(self.coordinator.device.on)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_command(self.coordinator.device.off)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        await self.coordinator.async_command(
            self.coordinator.device.set_mode,
            PRESET_TO_MODE[preset_mode],
        )
