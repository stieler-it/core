"""Constants for the tq_energymanager integration."""

from tqenergymanager300.tqenergymanager300 import (
    TQDATA_ACTIVE_ENERGY_FEEDIN,
    TQDATA_ACTIVE_ENERGY_PURCHASE,
    TQDATA_ACTIVE_POWER_FEEDIN,
    TQDATA_ACTIVE_POWER_PURCHASE,
    TQDATA_SUPPLY_FREQUENCY,
)

from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_UNIT_OF_MEASUREMENT,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
)

DOMAIN = "tq_energymanager"

CONF_SERIALNUMBER = "serialnumber"

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"


class SensorTypeEntry:
    """Definition of a sensor type offered by the Energy Meter."""

    def __init__(
        self,
        friendly_name: str,
        data_key: str,
        sensor_data: dict,
    ) -> None:
        """Create sensor type."""
        self.friendly_name = friendly_name
        self.data_key = data_key
        self.sensor_data = sensor_data


SENSOR_TYPES: list[SensorTypeEntry] = [
    SensorTypeEntry(
        "Purchase active power",
        TQDATA_ACTIVE_POWER_PURCHASE,
        {
            ATTR_DEVICE_CLASS: SensorDeviceClass.POWER,
            ATTR_UNIT_OF_MEASUREMENT: UnitOfPower.WATT,
            ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
        },
    ),
    SensorTypeEntry(
        "Purchase active energy",
        TQDATA_ACTIVE_ENERGY_PURCHASE,
        {
            ATTR_DEVICE_CLASS: SensorDeviceClass.ENERGY,
            ATTR_UNIT_OF_MEASUREMENT: UnitOfEnergy.WATT_HOUR,
            ATTR_STATE_CLASS: SensorStateClass.TOTAL_INCREASING,
        },
    ),
    SensorTypeEntry(
        "Feed-in active power",
        TQDATA_ACTIVE_POWER_FEEDIN,
        {
            ATTR_DEVICE_CLASS: SensorDeviceClass.POWER,
            ATTR_UNIT_OF_MEASUREMENT: UnitOfPower.WATT,
            ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
        },
    ),
    SensorTypeEntry(
        "Feed-in active energy",
        TQDATA_ACTIVE_ENERGY_FEEDIN,
        {
            ATTR_DEVICE_CLASS: SensorDeviceClass.ENERGY,
            ATTR_UNIT_OF_MEASUREMENT: UnitOfEnergy.WATT_HOUR,
            ATTR_STATE_CLASS: SensorStateClass.TOTAL_INCREASING,
        },
    ),
    SensorTypeEntry(
        "Supply frequency",
        TQDATA_SUPPLY_FREQUENCY,
        {
            ATTR_DEVICE_CLASS: SensorDeviceClass.FREQUENCY,
            ATTR_UNIT_OF_MEASUREMENT: UnitOfFrequency.HERTZ,
            ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
        },
    ),
]
