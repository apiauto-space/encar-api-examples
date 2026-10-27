"""Keep a local copy of a market in SQLite: one full import, then hourly change-feed polls.

This is the usual integration of an importer's site or bot: the site reads its own
database, and the API only brings what changed.

    pip install httpx
    export APIAUTO_KEY=...
    python sync_catalog.py kr --brand Kia --limit 20   # the demo key: up to 20 cars a page
    python sync_catalog.py cn                          # a whole market needs a paid quota

The change feed (/v1/changes) comes with Pro, Max and the demo key.
"""

import argparse
import json
import os
import sqlite3
import time
from datetime import datetime, timezone

import httpx

api = httpx.Client(
    base_url="https://api.apiauto.space/v1",
    headers={"X-API-Key": os.environ["APIAUTO_KEY"]},
    timeout=60,
)
db = sqlite3.connect("cars.db")
db.execute(
    """create table if not exists cars (
        id text primary key, market text, title text, price text, currency text,
        price_usd text, is_active integer, record text
    )"""
)
db.execute("create table if not exists sync (market text primary key, since text)")


def get(path: str, params: dict | None = None) -> dict:
    """GET with a pause on 429 (rate limit) and 503, as the docs recommend."""
    while True:
        response = api.get(path, params=params)
        if response.status_code in (429, 503):
            time.sleep(int(response.headers.get("Retry-After", "1")))
            continue
        response.raise_for_status()
        return response.json()


def save(car: dict) -> None:
    db.execute(
        "insert or replace into cars values (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            car["id"], car["market"], car["title"], car["price"]["amount"],
            car["price"]["currency"], car["price_usd"], int(car["is_active"]),
            json.dumps(car, ensure_ascii=False),
        ),
    )


def import_market(market: str, filters: dict, limit: int) -> None:
    """The first import: every page by the cursor. Each car returned is one record of quota."""
    params = {"market": market, "limit": limit, **filters}
    total = 0
    while True:
        page = get("/cars", params)
        for car in page["items"]:
            save(car)
        total += len(page["items"])
        db.commit()
        print(f"imported {total}")
        if not page["next_cursor"]:
            return
        params["cursor"] = page["next_cursor"]


def follow_changes(market: str, since: str, filters: dict, limit: int) -> str:
    """Apply every event since the last poll; returns the moment to ask from next time.
    The feed covers the whole market, so new cars are checked against our filters."""
    now = datetime.now(timezone.utc).isoformat()
    params = {"market": market, "since": since, "limit": limit}
    while True:
        page = get("/changes", params)
        for event in page["items"]:
            if event["type"] == "added":
                car = get(f"/cars/{event['car_id']}")
                if filters.get("brand") in (None, car["brand"]):
                    save(car)
            elif event["type"] == "disappeared":      # sold or withdrawn
                db.execute("update cars set is_active = 0 where id = ?", (event["car_id"],))
            else:                                     # price_drop, price_up
                db.execute(
                    "update cars set price = ? where id = ?",
                    (event["new_price"], event["car_id"]),
                )
        db.commit()
        print(f"{len(page['items'])} events")
        if not page["next_cursor"]:
            return now
        params["cursor"] = page["next_cursor"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("market", choices=["kr", "cn", "us"])
    parser.add_argument("--brand")
    parser.add_argument("--limit", type=int, default=100, help="20 on the demo key")
    args = parser.parse_args()
    filters = {"brand": args.brand} if args.brand else {}

    row = db.execute("select since from sync where market = ?", (args.market,)).fetchone()
    if row is None:
        since = datetime.now(timezone.utc).isoformat()
        import_market(args.market, filters, args.limit)
    else:
        since = row[0]

    while True:
        since = follow_changes(args.market, since, filters, args.limit)
        db.execute("insert or replace into sync values (?, ?)", (args.market, since))
        db.commit()
        time.sleep(3600)  # market copies are refreshed hourly; polling more often brings nothing
