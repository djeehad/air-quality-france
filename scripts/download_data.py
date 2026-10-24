"""Build data/processed/daily.parquet from the LCSQA "flux E2" daily CSV files.

Two ways to get the files:
  1. Automatic:  python scripts/download_data.py --start 2024-01-01 --every 7
     downloads one day out of N (default: one per week) from DAILY_FILE_URL.
  2. Manual:     put FR_E2_YYYY-MM-DD.csv files in data/raw/, then
                 python scripts/download_data.py --local

Each day is reduced to daily means and cached in data/processed/days/ (a few KB),
so the 12 MB raw CSV can be deleted (--keep-raw to keep it).
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import constants as C  # noqa: E402

DAYS_DIR = C.PROCESSED_DIR / "days"
KEYS = ["date", "code_site", "site", "zone", "setting", "influence", "pollutant"]


def to_daily(path: Path) -> pd.DataFrame:
    """One raw hourly CSV -> daily mean per station and pollutant."""
    h = pd.read_csv(path, sep=";", encoding="utf-8-sig", low_memory=False,
                    usecols=lambda c: c in C.COLUMN_MAP)
    h = h.rename(columns=C.COLUMN_MAP)
    h = h[h["pollutant"].isin(C.POLLUTANTS)]
    h["value"] = pd.to_numeric(h["value"], errors="coerce")
    # validité: 1 = valid, 4 = not yet validated (kept), -1 = invalid (dropped)
    h.loc[h["validity"] == -1, "value"] = pd.NA
    h["date"] = pd.to_datetime(h["start"], format="%Y/%m/%d %H:%M:%S").dt.normalize()
    return (h.groupby(KEYS, as_index=False)
              .agg(value=("value", "mean"), n_hours=("value", "count")))


def process(path: Path, keep_raw: bool) -> bool:
    out = DAYS_DIR / f"{path.stem}.parquet"
    try:
        to_daily(path).to_parquet(out, index=False)
    except Exception as exc:  # a corrupt or unexpected file should not stop the run
        print(f"  skip {path.name}: {exc}")
        return False
    if not keep_raw:
        path.unlink()
    return True


def download(day: date) -> Path | None:
    path = C.RAW_DIR / f"FR_E2_{day}.csv"
    url = C.DAILY_FILE_URL.format(year=day.year, date=day.isoformat())
    try:
        r = requests.get(url, timeout=120)
    except requests.RequestException as exc:
        print(f"  {day}: {exc}")
        return None
    if r.status_code != 200:
        print(f"  {day}: HTTP {r.status_code}")
        return None
    path.write_bytes(r.content)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2024-01-01", help="first day (YYYY-MM-DD)")
    ap.add_argument("--end", default=None, help="last day (default: yesterday)")
    ap.add_argument("--every", type=int, default=7, help="keep one day out of N (7 = weekly)")
    ap.add_argument("--local", action="store_true", help="only process CSV files already in data/raw")
    ap.add_argument("--keep-raw", action="store_true")
    args = ap.parse_args()
    for d in (C.RAW_DIR, DAYS_DIR):
        d.mkdir(parents=True, exist_ok=True)

    if args.local:
        for p in sorted(C.RAW_DIR.glob("FR_E2_*.csv")):
            print(f"processing {p.name}")
            process(p, keep_raw=True)
    else:
        start = date.fromisoformat(args.start)
        end = date.fromisoformat(args.end) if args.end else date.today() - timedelta(days=1)
        day = start
        while day <= end:
            if (DAYS_DIR / f"FR_E2_{day}.parquet").exists():
                print(f"{day}: cached")
            else:
                print(f"{day}: downloading")
                if (p := download(day)):
                    process(p, args.keep_raw)
            day += timedelta(days=args.every)

    files = sorted(DAYS_DIR.glob("*.parquet"))
    if not files:
        sys.exit("No data. Check DAILY_FILE_URL in utils/constants.py or use --local.")
    daily = pd.concat((pd.read_parquet(f) for f in files), ignore_index=True)
    daily.to_parquet(C.DAILY_PARQUET, index=False)
    print(f"\nSaved {len(daily):,} rows ({len(files)} days, {daily['code_site'].nunique()} stations) "
          f"-> {C.DAILY_PARQUET}")


if __name__ == "__main__":
    main()
