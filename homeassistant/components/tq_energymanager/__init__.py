"""The tq_energymanager integration."""
import asyncio
from datetime import timedelta
import logging

import async_timeout
from tqenergymanager300.tqenergymanager300 import TqEnergyManagerJsonClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SERIALNUMBER, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the tq_energymanager component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up tq_energymanager from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    client = TqEnergyManagerJsonClient(
        entry.data[CONF_HOST],
        entry.data[CONF_SERIALNUMBER],
        entry.data[CONF_PASSWORD],
    )

    try:
        # authenticated =
        await hass.async_add_executor_job(client.login)
        # authenticated = await client.login()
    except Exception as exception:  # aiohttp.ClientError as exception:
        _LOGGER.warning(exception)
        raise ConfigEntryNotReady from exception

    async def async_update_data() -> dict:
        """Fetch data from TQ Energy Manager."""
        async with async_timeout.timeout(10):
            try:
                return await hass.async_add_executor_job(client.fetch_data)
                # return await client.fetch_data()
            except Exception as exception:  # aiohttp.ClientError as exception:
                raise UpdateFailed(exception) from exception

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=60),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    # Fetch initial data in case we need it during entities subscribe
    # await coordinator.async_refresh()

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok