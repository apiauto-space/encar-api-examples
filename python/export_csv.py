"""Export a filtered selection of cars to CSV (opens in Excel and Google Sheets).

    pip install httpx
    export APIAUTO_KEY=...
    python export_csv.py kr --brand Genesis --year-min 2022 --max 200 > genesis.csv

Every car exported is one record of quota; --max keeps the export small.
"""

import argparse
import csv
import os
import sys

import httpx

parser = argparse.ArgumentParser()
parser.add_argument("market", choices=["kr", "cn", "us"])
parser.add_argument("--brand")
parser.add_argument("--model")
parser.add_argument("--year-min", type=int)
parser.add_argument("--price-usd-max", type=float)
parser.add_argument("--max", type=int, default=100, help="stop after this many cars")
parser.add_argument("--limit", type=int, default=20, help="cars per page: 20 on the demo, up to 100")
args = parser.parse_args()

api = httpx.Client(
    base_url="https://api.apiauto.space/v1",
    headers={"X-API-Key": os.environ["APIAUTO_KEY"]},
    timeout=60,
)
params = {
    "market": args.market,
    "brand": args.brand,
    "model": args.model,
    "year_min": args.year_min,
    "price_usd_max": args.price_usd_max,
    "limit": min(args.limit, args.max),
}
params = {key: value for key, value in params.items() if value is not None}

columns = [
    "id", "title", "brand", "model", "generation", "trim", "year", "mileage_km", "fuel",
    "transmission", "engine_cc", "body_type", "color", "vin", "price", "currency", "price_usd",
    "region", "city", "photo_count", "listing_url", "first_seen_at",
]
writer = csv.DictWriter(sys.stdout, fieldnames=columns, extrasaction="ignore")
writer.writeheader()

written = 0
while written < args.max:
    page = api.get("/cars", params=params).raise_for_status().json()
    for car in page["items"][: args.max - written]:
        writer.writerow({
            **car,
            "price": car["price"]["amount"],
            "currency": car["price"]["currency"],
            "region": car["location"]["region"],
            "city": car["location"]["city"],
        })
        written += 1
    if not page["next_cursor"]:
        break
    params["cursor"] = page["next_cursor"]

print(f"exported {written} cars", file=sys.stderr)
