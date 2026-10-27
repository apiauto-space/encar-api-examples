"""One model in three markets: Korea (Encar), China (Che168) and US auctions (Copart, IAAI).

The record format is the same everywhere, so one loop prints all three. price_usd is the
price converted at the ECB daily rate, which makes markets comparable. The price floor skips
cars without a price (many US lots have no buy-now price) and Encar leases listed with a
monthly payment instead of a price.

    pip install httpx
    export APIAUTO_KEY=...
    python compare_markets.py Toyota Camry
"""

import os
import statistics
import sys
from decimal import Decimal

import httpx

brand = sys.argv[1] if len(sys.argv) > 1 else "Toyota"
model = sys.argv[2] if len(sys.argv) > 2 else "Camry"

api = httpx.Client(
    base_url="https://api.apiauto.space/v1",
    headers={"X-API-Key": os.environ["APIAUTO_KEY"]},
    timeout=30,
)

for market, source in (("kr", "Encar"), ("cn", "Che168"), ("us", "Copart + IAAI")):
    page = api.get(
        "/cars",
        params={
            "market": market,
            "brand": brand,
            "model": model,
            "year_min": 2020,
            "price_usd_min": 3000,
            "limit": 20,
        },
    ).raise_for_status().json()

    prices = [Decimal(car["price_usd"]) for car in page["items"] if car["price_usd"]]
    median = f"${statistics.median(prices):,.0f}" if prices else "no prices"
    print(f"\n{source}: {page['count'] if page['count'] is not None else '10,000+'} cars, "
          f"median of the newest {len(prices)}: {median}")
    for car in page["items"][:3]:
        print(f"  {car['title']} · {car['mileage_km']} km · ${car['price_usd']}")
