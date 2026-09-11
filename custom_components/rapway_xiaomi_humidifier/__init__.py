"""Rapway Xiaomi Humidifier integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, PLATFORMS
from .coordinator import XiaomiHumidifierCoordinator


def _remove_legacy_entities(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove legacy fan and target humidity entities from v0.2.x."""
    registry = er.async_get(hass)

    legacy_entities = (
        ("fan", f"{entry.entry_id}_fan"),
        ("number", f"{entry.entry_id}_target_humidity"),
    )

    for platform, unique_id in legacy_entities:
        entity_id = registry.async_get_entity_id(
            platform,
            DOMAIN,
            unique_id,
        )

        if entity_id is not None:
            registry.async_remove(entity_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""
    _remove_legacy_entities(hass, entry)

    coordinator = XiaomiHumidifierCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
