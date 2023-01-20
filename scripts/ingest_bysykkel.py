import os
from datetime import datetime

import requests

BASE_URL = "https://gbfs.urbansharing.com"
LOCALE = "oslobysykkel.no"
FILE_NAMES = ["station_information", "station_status"]
OUTDIR = "./data"

timestamp = str(datetime.now().date()).replace(" ", "_")

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

for file in FILE_NAMES:
    r = requests.get(f"{BASE_URL}/{LOCALE}/{file}.json")
    with open(f"{OUTDIR}/{file}_{timestamp}.json", "w") as f:
        f.writelines(r.text)
        f.close()
