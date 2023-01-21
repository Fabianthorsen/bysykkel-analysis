import enum
import os
import shutil
import zipfile
from io import BytesIO
from urllib import error
from urllib.request import urlopen
from zipfile import ZipFile

BASE_URL = "https://data-legacy.urbansharing.com"
ENDPOINT = "oslobysykkel.no"
OUTDIR = "./data/trips/legacy"
YEARS = [2016, 2017, 2018]
MONTHS = range(1, 13)


for year in YEARS:
    subdir = f"{OUTDIR}/{year}"

    for month in MONTHS:
        filename = f"{month:02d}.json"

        url = f"{BASE_URL}/{ENDPOINT}/{year}/{filename}.zip"

        if not os.path.isfile(f"{subdir}/{filename}"):
            try:
                resp = urlopen(url)

                with ZipFile(BytesIO(resp.read())) as zip_file:
                    for file_info in zip_file.infolist():

                        if file_info.is_dir():
                            continue

                        file_path = file_info.filename
                        extracted_path = os.path.join(subdir, file_path)
                        os.makedirs(os.path.dirname(extracted_path), exist_ok=True)

                        with open(extracted_path, "wb") as dest:
                            with zip_file.open(file_info, "r") as source:
                                shutil.copyfileobj(source, dest)

                    zip_file.close()

            except error.HTTPError:
                pass
