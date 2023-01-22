import os
from datetime import datetime

import requests

BASE_URL = "https://data.urbansharing.com"
ENDPOINT = "oslobysykkel.no/trips/v1"
OUTDIR = "./data/trips/v1"
YEARS = [2019, 2020, 2021, 2022, 2023]
MONTHS = range(1, 13)

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

# TODO: Rewrite with urllib
for year in YEARS:
    if not os.path.exists(f"{OUTDIR}/{year}/"):
        os.mkdir(f"{OUTDIR}/{year}/")

        for month in MONTHS:
            r = requests.get(f"{BASE_URL}/{ENDPOINT}/{year}/{month:02d}.json")
            if r.status_code == 200:
                with open(f"{OUTDIR}/{year}/{month:02d}.json", "w") as f:
                    f.writelines(r.text)
                    f.close()
