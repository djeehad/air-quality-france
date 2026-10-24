"""Build data/stations.csv (code_site, municipality, lat, lon, area) from the LCSQA station metadata.

The metadata file ("D" file, .xls) is listed under "fichiers de documentation" on the dataset page:
https://www.data.gouv.fr/datasets/5b98b648634f415309d52a50

Usage:  python scripts/build_stations.py path/to/fr-2026-d-xxxxxxxx.xls
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import constants as C  # noqa: E402


def main(xls: str) -> None:
    st = pd.read_excel(xls, sheet_name="AirQualityStations")
    st = st.rename(columns={"NatlStationCode": "code_site", "Latitude": "lat",
                            "Longitude": "lon", "Municipality": "municipality"})
    st["area"] = st["AreaClassification"].astype(str).str.rsplit("/", n=1).str[-1]
    # a station can appear in several versions: keep the latest
    st = (st.sort_values("Version").drop_duplicates("code_site", keep="last")
            [["code_site", "municipality", "lat", "lon", "area"]])
    st.to_csv(C.STATIONS_CSV, index=False)
    print(f"Saved {len(st)} stations -> {C.STATIONS_CSV}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
