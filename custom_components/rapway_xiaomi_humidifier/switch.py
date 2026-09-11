"""Switch platform for Rapway Xiaomi Humidifier."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from homeassistant.components.switch import SwitchEntity

from .entity import XiaomiHumidifierEntity


@dataclass(frozen=True)
class SwitchDescription:
    key: str
    name: str
    icon: str
    value_fn: Callable
    method_name: str


SWITCHES = (
    SwitchDescription(
        "led",
        "LED",
        "mdi:led-on",
        lambda s: bool(s.led_light),
        "set_light",
    ),
    SwitchDescription(
        "buzzer",
        "Buzzer",
        "mdi:volume-high",
        lambda s: bool(s.buzzer),
        "set_buzzer",
    ),
    SwitchDescription(
        "overwet_protection",
        "Overwet protection",
        "mdi:water-alert",
        lambda s: bool(s.overwet_protect),
        "set_overwet_protect",
    ),
)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        XiaomiHumidifierSwitch(coordinator, description)
        for description in SWITCHES
    )


class XiaomiHumidifierSwitch(XiaomiHumidifierEntity, SwitchEntity):
    def __init__(self, coordinator, description: SwitchDescription) -> None:
        super().__init__(coordinator, description.key)
        self.description = description
        self._attr_name = description.name
        self._attr_icon = description.icon

    @property
    def is_on(self):
        return self.description.value_fn(self.coordinator.data)

    async def async_turn_on(self, **kwargs) -> None:
        method = getattr(self.coordinator.device, self.description.method_name)
        await self.coordinator.async_command(method, True)

    async def async_turn_off(self, **kwargs) -> None:
        method = getattr(self.coordinator.device, self.description.method_name)
        await self.coordinator.async_command(method, False)
