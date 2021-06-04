"""Constants for the tq_energymanager integration."""

from typing import List

from tqenergymanager300.tqenergymanager300 import (
    TQDATA_ACTIVE_ENERGY_FEEDIN,
    TQDATA_ACTIVE_ENERGY_PURCHASE,
    TQDATA_ACTIVE_POWER_FEEDIN,
    TQDATA_ACTIVE_POWER_PURCHASE,
    TQDATA_SUPPLY_FREQUENCY,
)

from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    ENERGY_WATT_HOUR,
    FREQUENCY_HERTZ,
    POWER_WATT,
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
        device_class: str,
        unit_of_measurement: str,
    ):
        """Create sensor type."""
        self.friendly_name = friendly_name
        self.device_class = device_class
        self.data_key = data_key
        self.unit_of_measurement = unit_of_measurement


SENSOR_TYPES: List[SensorTypeEntry] = [
    SensorTypeEntry(
        "Purchase active power",
        TQDATA_ACTIVE_POWER_PURCHASE,
        DEVICE_CLASS_POWER,
        POWER_WATT,
    ),
    SensorTypeEntry(
        "Purchase active energy",
        TQDATA_ACTIVE_ENERGY_PURCHASE,
        DEVICE_CLASS_ENERGY,
        ENERGY_WATT_HOUR,
    ),
    SensorTypeEntry(
        "Feed-in active power",
        TQDATA_ACTIVE_POWER_FEEDIN,
        DEVICE_CLASS_POWER,
        POWER_WATT,
    ),
    SensorTypeEntry(
        "Feed-in active energy",
        TQDATA_ACTIVE_ENERGY_FEEDIN,
        DEVICE_CLASS_ENERGY,
        ENERGY_WATT_HOUR,
    ),
    SensorTypeEntry("Supply frequency", TQDATA_SUPPLY_FREQUENCY, None, FREQUENCY_HERTZ),
]
