import enum
import json
import os
import zipfile
from io import BytesIO
from urllib import error
from urllib.request import urlopen
from zipfile import ZipFile

BASE_URL = "https://data-legacy.urbansharing.com"
ENDPOINT = "oslobysykkel.no"
OUTDIR = "./data/trips/legacy"


class ResponseCode(enum.Enum):
    OK = 200
    NOT_FOUND = 404

    def __eq__(self, other):
        return self.value == other


if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

for year in range(2016, 2019):
    subdir = f"{OUTDIR}/{year}/"

    if not os.path.exists(subdir):
        os.mkdir(subdir)

    for month in range(1, 13):
        filename = f"{month:02d}.json"
        url = f"{BASE_URL}/{ENDPOINT}/{year}/{filename}.zip"

        if not os.path.isfile(f"{subdir}/{filename}"):
            try:
                resp = urlopen(url)
                with ZipFile(BytesIO(resp.read())) as zip_file:
                    for file in zip_file.namelist():
                        zip_file.extract(file, f"{subdir}/{filename}")

                    zip_file.close()

            except error.HTTPError:
                pass
