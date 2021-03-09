"""Platform for sensor integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DATA_COORDINATOR, DOMAIN, SENSOR_TYPES, SensorTypeEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the sensor platform."""

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    # TODO: we could check coordinator.data for the initial response (if some entries are not always present)

    entities = []

    for sensor in SENSOR_TYPES:
        entities.append(EnergyMeterSensor(coordinator, sensor))

    # entities.append(
    #    EnergyMeterSensor(coordinator, TQDATA_ACTIVE_POWER_INCOMING, POWER_WATT)
    # )
    # entities.append(
    #    EnergyMeterSensor(coordinator, TQDATA_ACTIVE_POWER_MINUS, POWER_WATT)
    # )

    # Fetch initial data so we have data when entities subscribe
    # await coordinator.async_refresh()

    async_add_entities(entities, True)
    #    EnergyMeterSensor(coordinator, key, POWER_WATT)
    #    for key, entity in enumerate(coordinator.data)
    # )
    # async_add_entities([EnergyMeterSensor()])
    # add_entities(AwesomeLight(light) for light in hub.lights())


# async def async_setup_entry(
#    hass: HomeAssistantType, config_entry: ConfigEntry, async_add_entities
# ) -> None:
#    """Setup the sensor platform by config entry."""
#    return await async_setup_platform(
#        hass, config_entry.data, async_add_entities, discovery_info=None
#    )


class EnergyMeterSensor(CoordinatorEntity, Entity):
    """Representation of a Sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator, sensor: SensorTypeEntry):
        """Initialize the sensor."""
        self.friendly_name = sensor.friendly_name
        self.data_key = sensor.data_key
        self._unit_of_measurement = sensor.unit_of_measurement

        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "TQ " + self.friendly_name

    @property
    def state(self):
        """Return the state of the sensor."""
        data: object = self.coordinator.data
        if data is None or self.data_key not in data:
            return None
        return data[self.data_key]

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._unit_of_measurement
