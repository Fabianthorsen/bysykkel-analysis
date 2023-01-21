import os
from datetime import datetime

import requests

BASE_URL = "https://data.urbansharing.com"
ENDPOINT = "oslobysykkel.no/trips/v1"
OUTDIR = "./data/trips/v1"
TIMESTAMP = datetime.now().date()

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

for year in range(2019, 2024):
    if not os.path.exists(f"{OUTDIR}/{year}/"):
        os.mkdir(f"{OUTDIR}/{year}/")

        for month in range(1,13): 
            r = requests.get(f"{BASE_URL}/{ENDPOINT}/{year}/{month:02d}.json")
            if r.status_code == 200:
                with open(f"{OUTDIR}/{year}/{month:02d}.json", "w") as f:
                    f.writelines(r.text)
                    f.close()
