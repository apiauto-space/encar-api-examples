"""Search Encar (South Korea) by make, model and year and print the cars.

    pip install httpx
    export APIAUTO_KEY=...        # the demo key from https://t.me/apiautospace_bot?start=demo
    python first_request.py
"""

import os

import httpx

api = httpx.Client(
    base_url="https://api.apiauto.space/v1",
    headers={"X-API-Key": os.environ["APIAUTO_KEY"]},
    timeout=30,
)

response = api.get(
    "/cars",
    params={
        "market": "kr",          # kr = Encar, cn = Che168, us = Copart and IAAI
        "brand": "Hyundai",
        "model": "Grandeur",     # the model family; Korea's generation is a separate field
        "year_min": 2020,
        "price_usd_min": 5000,   # skips leases that Encar lists with a monthly payment
        "sort": "-first_seen",   # newest listings first (the default)
        "limit": 20,             # up to 20 on the demo key, up to 100 on paid plans
    },
)
response.raise_for_status()
page = response.json()

print(f"{page['count']} cars match, showing {len(page['items'])}")
for car in page["items"]:
    price = car["price"]
    print(
        f"{car['id']:<18} {car['title']:<50} "
        f"{car['mileage_km'] or '?':>7} km  "
        f"{price['amount']} {price['currency']} (≈ ${car['price_usd']})"
    )

# Every answer says how much quota is left and how old the market copy is.
print("records left:", response.headers.get("X-Quota-Remaining"))
print("data age, s:", response.headers.get("X-Data-Age-Seconds"))
