"""Constants for the tq_energymanager integration."""

from typing import List

from homeassistant.const import ENERGY_WATT_HOUR, FREQUENCY_HERTZ, POWER_WATT

from .api import (
    TQDATA_ACTIVE_ENERGY_FEEDIN,
    TQDATA_ACTIVE_ENERGY_PURCHASE,
    TQDATA_ACTIVE_POWER_FEEDIN,
    TQDATA_ACTIVE_POWER_PURCHASE,
    TQDATA_SUPPLY_FREQUENCY,
)

DOMAIN = "tq_energymanager"

CONF_SERIALNUMBER = "serialnumber"

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"


class SensorTypeEntry:
    """Definition of a sensor type offered by the Energy Meter."""

    def __init__(self, friendly_name: str, data_key: str, unit_of_measurement: str):
        """Create sensor type."""
        self.friendly_name = friendly_name
        self.data_key = data_key
        self.unit_of_measurement = unit_of_measurement


SENSOR_TYPES: List[SensorTypeEntry] = [
    SensorTypeEntry("Purchase active power", TQDATA_ACTIVE_POWER_PURCHASE, POWER_WATT),
    SensorTypeEntry(
        "Purchase active energy", TQDATA_ACTIVE_ENERGY_PURCHASE, ENERGY_WATT_HOUR
    ),
    SensorTypeEntry("Feed-in active power", TQDATA_ACTIVE_POWER_FEEDIN, POWER_WATT),
    SensorTypeEntry(
        "Feed-in active energy", TQDATA_ACTIVE_ENERGY_FEEDIN, ENERGY_WATT_HOUR
    ),
    SensorTypeEntry("Supply frequency", TQDATA_SUPPLY_FREQUENCY, FREQUENCY_HERTZ),
]
