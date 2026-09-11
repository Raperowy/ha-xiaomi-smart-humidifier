"""Config flow for Rapway Xiaomi Humidifier."""

from __future__ import annotations

import re

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from miio import AirHumidifierJsqs, DeviceException

from .const import CONF_TOKEN, DEFAULT_NAME, DOMAIN, MODEL

TOKEN_RE = re.compile(r"^[0-9a-fA-F]{32}$")


class RapwayXiaomiHumidifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            token = user_input[CONF_TOKEN].strip()

            if not TOKEN_RE.fullmatch(token):
                errors[CONF_TOKEN] = "invalid_token"
            else:
                device = AirHumidifierJsqs(host, token, model=MODEL)
                try:
                    status = await self.hass.async_add_executor_job(device.status)
                    if status is None:
                        raise DeviceException("Empty status")
                except Exception:
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(f"{MODEL}_{host}")
                    self._abort_if_unique_id_configured(
                        updates={CONF_HOST: host, CONF_TOKEN: token}
                    )

                    return self.async_create_entry(
                        title=DEFAULT_NAME,
                        data={
                            CONF_HOST: host,
                            CONF_TOKEN: token,
                        },
                    )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_TOKEN): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
