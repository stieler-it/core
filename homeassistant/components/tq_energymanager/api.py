"""Client for TQ Energy Manager JSON API."""
import json

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; "}

TQDATA_ACTIVE_POWER_PURCHASE = "active_power_purchase"
TQDATA_ACTIVE_ENERGY_PURCHASE = "active_energy_purchase"
TQDATA_ACTIVE_POWER_FEEDIN = "active_power_feedin"
TQDATA_ACTIVE_ENERGY_FEEDIN = "active_energy_feedin"
TQDATA_SUPPLY_FREQUENCY = "supply_frequency"


class TqEnergyManagerJsonApi:
    """Client to access JSON API of Energy Manager 300."""

    def __init__(self, hostname, serialNumber, password):
        """Create object."""
        self.hostname = hostname
        self.serialNumber = serialNumber
        self.password = password

    def login(self) -> bool:
        """Login to JSON API."""
        self.session = requests.Session()

        # Initial handshake

        r1 = self.session.get("http://" + self.hostname + "/start.php", headers=HEADERS)
        if r1.status_code != requests.codes.ok:
            return False

        login_params = {
            "login": self.serialNumber,
            "password": self.password,
            "save_login": "1",
        }
        r2 = self.session.post(
            "http://" + self.hostname + "/start.php", login_params, headers=HEADERS
        )

        return r2.status_code == requests.codes.ok

    def fetch_data(self) -> dict:
        """Fetch data from Energy Manager."""

        r3 = self.session.get(
            "http://" + self.hostname + "/mum-webservice/data.php", headers=HEADERS
        )
        if r3.status_code == requests.codes.ok:
            pass
        else:
            Error_Connecting = r3.status_code
            print("Unable to Get data :", Error_Connecting)
        em300data = json.loads(r3.text)

        result = {}
        # Currently we assume it is an EM300 with fields as described in the docs at
        # https://www.tq-group.com/filedownloads/files/products/automation/manuals/EM300_sensorbars/spezifikationen/TQ_EM_JSON-API.0104.pdf
        result[TQDATA_ACTIVE_POWER_PURCHASE] = em300data.pop("1-0:1.4.0*255")
        result[TQDATA_ACTIVE_ENERGY_PURCHASE] = em300data.pop("1-0:1.8.0*255")
        result[TQDATA_ACTIVE_POWER_FEEDIN] = em300data.pop("1-0:2.4.0*255")
        result[TQDATA_ACTIVE_ENERGY_FEEDIN] = em300data.pop("1-0:2.8.0*255")
        result[TQDATA_SUPPLY_FREQUENCY] = em300data.pop("1-0:14.4.0*255")
        return result
