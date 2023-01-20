import json
import os
from dataclasses import dataclass, field
from datetime import datetime

import requests

BASE_URL = "https://gbfs.urbansharing.com"
LOCALE = "oslobysykkel.no"
FILE_NAMES = ["station_information", "station_status"]
OUTDIR = "./data"


@dataclass
class Station:
    station_id: int
    name: str
    address: str
    rental_uris: dict[str, str]
    lat: float
    lon: float
    capacity: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class StationStatus:
    station_id: int
    is_installed: int
    is_renting: int
    is_returning: int
    last_reported: int
    num_bikes_available: int
    num_docks_available: int


if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

for file in FILE_NAMES:
    r = requests.get(f"{BASE_URL}/{LOCALE}/{file}.json")
    if file == "station_information":
        stations = r.json()["data"]["stations"]
        for station in stations:
            s = Station(
                station["station_id"],
                station["name"],
                station["address"],
                station["rental_uris"],
                station["lat"],
                station["lon"],
                station["capacity"],
            )
            print(s.rental_uris)


    # with open(f"{OUTDIR}/{file}_{TIMESTAMP}.json", "w") as f:
    #    f.writelines(r.text)
    #    f.close()
