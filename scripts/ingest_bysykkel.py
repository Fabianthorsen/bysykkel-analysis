import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC

import requests

BASE_URL = "https://gbfs.urbansharing.com"
LOCALE = "oslobysykkel.no"
FILE_NAMES = ["station_information", "station_status"]
OUTDIR = "./data"
TIMESTAMP = datetime.now()

class Writable(ABC):
    def write_json(self, outdir) -> None:
        pass


@dataclass
class Station:
    station_id: int
    name: str
    address: str
    rental_uris: dict[str, str]
    lat: float
    lon: float
    capacity: int
    source: str
    timestamp: datetime = field(default=TIMESTAMP)


@dataclass
class StationStatus:
    station_id: int
    is_installed: int
    is_renting: int
    is_returning: int
    last_reported: int
    num_bikes_available: int
    num_docks_available: int
    source: str 
    timestamp: datetime = field(default=TIMESTAMP)


@dataclass
class StationDB:
    stations: list[Station] = field(default_factory=list)

    def insert_row(self, row: Station):
       self.stations.append(row) 


@dataclass
class StatusDB:
    statuses: list[StationStatus] = field(default_factory=list)

    def insert_row(self, row: StationStatus):
       self.statuses.append(row) 

stations_table = StationDB()
status_table = StatusDB()

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

for file in FILE_NAMES:
    r = requests.get(f"{BASE_URL}/{LOCALE}/{file}.json")
    entries = r.json()["data"]["stations"]

    if file == "station_information":
        for station in entries:
            s = Station(
                station_id=station["station_id"],
                name=station["name"],
                address=station["address"],
                rental_uris=station["rental_uris"],
                lat=station["lat"],
                lon=station["lon"],
                capacity=station["capacity"],
                source=f"{BASE_URL}/{LOCALE}/{file}"
            )
            stations_table.insert_row(s)

    if file == "station_status":
        for status in entries:
            s = StationStatus(
                station_id=station["station_id"],
                is_installed=status["is_installed"],
                is_renting=status["is_renting"],
                is_returning=status["is_returning"],
                last_reported=status["last_reported"],
                num_bikes_available=status["num_bikes_available"],
                num_docks_available=status["num_docks_available"],
                source=f"{BASE_URL}/{LOCALE}/{file}"
            )
            status_table.insert_row(s)

    print(stations_table)
    print(status_table)
    
    # with open(f"{OUTDIR}/{file}_{TIMESTAMP}.json", "w") as f:
    #    f.writelines(r.text)
    #    f.close()
