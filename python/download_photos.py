"""Download the photos of one car.

Photo links in a record are signed and live about a day, so keep the car id and ask for
a fresh record when you need the photos again. Photo requests do not spend quota.

    pip install httpx
    export APIAUTO_KEY=...
    python download_photos.py encar:43020826
"""

import os
import sys
from pathlib import Path

import httpx

car_id = sys.argv[1] if len(sys.argv) > 1 else "encar:43020826"

api = httpx.Client(
    base_url="https://api.apiauto.space/v1",
    headers={"X-API-Key": os.environ["APIAUTO_KEY"]},
    timeout=30,
)
car = api.get(f"/cars/{car_id}").raise_for_status().json()

folder = Path(car_id.replace(":", "-"))
folder.mkdir(exist_ok=True)
with httpx.Client(timeout=60, follow_redirects=True) as http:  # /img may redirect to the source
    for number, url in enumerate(car["photos"], start=1):
        image = http.get(url).raise_for_status()
        (folder / f"{number:02}.jpg").write_bytes(image.content)
        print(f"{folder}/{number:02}.jpg  {len(image.content) // 1024} KB")

print(f"{car['title']}: {len(car['photos'])} of {car['photo_count']} photos")
