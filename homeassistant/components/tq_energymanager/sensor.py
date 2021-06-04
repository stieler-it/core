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

    entities = []

    for sensor in SENSOR_TYPES:
        entities.append(EnergyMeterSensor(coordinator, sensor))

    async_add_entities(entities, True)


class EnergyMeterSensor(CoordinatorEntity, Entity):
    """Representation of a Sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator, sensor: SensorTypeEntry):
        """Initialize the sensor."""
        self.friendly_name = sensor.friendly_name
        self._device_class = sensor.device_class
        self.data_key = sensor.data_key
        self._unit_of_measurement = sensor.unit_of_measurement

        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "TQ " + self.friendly_name

    @property
    def device_class(self):
        """Return the devices' class."""
        return self._device_class

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
