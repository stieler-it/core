"""Platform for TQ Energy Manager sensors."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_DEVICE_CLASS, ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    CONF_SERIALNUMBER,
    DATA_COORDINATOR,
    DOMAIN,
    SENSOR_TYPES,
    SensorTypeEntry,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    entities = []

    for sensor in SENSOR_TYPES:
        entities.append(
            EnergyMeterSensor(coordinator, sensor, entry.data[CONF_SERIALNUMBER])
        )

    async_add_entities(entities, True)


class EnergyMeterSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Energy Manager data Sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        sensor: SensorTypeEntry,
        device_serial: str,
    ) -> None:
        """Initialize the sensor."""
        self._friendly_name = sensor.friendly_name
        self._data_key = sensor.data_key
        self._sensor_data = sensor.sensor_data
        self._device_serial = device_serial

        super().__init__(coordinator)

    @property
    def unique_id(self) -> str:
        """Return the unique id of this Sensor Entity."""
        return f"{self._device_serial}_{self._data_key}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "TQ " + self._friendly_name

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return self._sensor_data.get(ATTR_DEVICE_CLASS)

    @property
    def state_class(self) -> str | None:
        """Return the class of the state of this device, from component STATE_CLASSES."""
        return self._sensor_data.get(ATTR_STATE_CLASS)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of this Sensor Entity or None."""
        return self._sensor_data.get(ATTR_UNIT_OF_MEASUREMENT)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data[self._data_key]
