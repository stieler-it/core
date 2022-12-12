"""Config flow for tq_energymanager integration."""
import logging
from urllib.parse import urlparse

import requests
from tqenergymanager300.tqenergymanager300 import TqEnergyManagerJsonClient
import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.components import ssdp
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_SERIALNUMBER, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {CONF_HOST: str, CONF_SERIALNUMBER: str, CONF_PASSWORD: str}
)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    client = TqEnergyManagerJsonClient(
        data[CONF_HOST], data[CONF_SERIALNUMBER], data[CONF_PASSWORD]
    )

    try:
        # Since API is not async, we pass it to the executor
        response = await hass.async_add_executor_job(client.login)
        if not response:
            raise InvalidAuth
    except requests.exceptions.ConnectionError as exc:
        raise CannotConnect from exc

    # Return info that you want to store in the config entry.
    return {"title": "Energy Manager 300"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for tq_energymanager."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize the config flow."""
        self.ssdp_info = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_ssdp(self, discovery_info: ssdp.SsdpServiceInfo) -> FlowResult:
        """Handle the SSDP discovery step."""

        _LOGGER.debug("async_step_ssdp: discovery_info: %s", discovery_info)

        host = urlparse(discovery_info.ssdp_location).hostname
        serial_number = discovery_info.upnp.get(ssdp.ATTR_UPNP_SERIAL)

        await self.async_set_unique_id(serial_number)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        # Remember for next step
        ssdp_info = {}
        ssdp_info[CONF_HOST] = host
        ssdp_info[CONF_SERIALNUMBER] = serial_number
        self.ssdp_info = ssdp_info

        return await self.async_step_ssdp_user()

    async def async_step_ssdp_user(self, user_input=None) -> FlowResult:
        """Reduced configuration step after SSDP."""

        ssdp_user_data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=self.ssdp_info[CONF_HOST]): str,
                CONF_PASSWORD: str,
            }
        )

        if user_input is None:
            return self.async_show_form(
                step_id="ssdp_user", data_schema=ssdp_user_data_schema
            )

        config_data = user_input
        config_data[CONF_SERIALNUMBER] = self.ssdp_info[CONF_SERIALNUMBER]

        errors = {}

        try:
            info = await validate_input(self.hass, config_data)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=config_data)

        return self.async_show_form(
            step_id="ssdp_user", data_schema=ssdp_user_data_schema, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
