# Encar API, Che168 API, Copart and IAAI API examples

Working examples for **[apiauto.space](https://apiauto.space/en/)**, a REST API with used-car
listings from **Encar** (South Korea), **Che168** (China) and the **Copart** and **IAAI** auctions
(USA) in one normalized JSON format. You get the same fields for every market, a change feed of new
cars, sold cars and price changes, and photos through one key in one header. The examples are in
curl, Python, JavaScript (Node.js) and PHP and work with a free demo key.

[![Get a free demo key](https://img.shields.io/badge/demo_key-free%2C_1_day-2AABEE?logo=telegram)](https://t.me/apiautospace_bot?start=demo)
[![Docs](https://img.shields.io/badge/docs-apiauto.space-111)](https://apiauto.space/en/docs/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-6BA539?logo=openapiinitiative)](https://api.apiauto.space/openapi.json)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/apiauto-space/encar-api-examples/blob/main/LICENSE)

> Encar, Che168, Copart and IAAI have no public API for their listings. apiauto.space keeps an
> hourly-refreshed copy of each catalog and serves it as one API. It is an independent service,
> not affiliated with Encar, Che168 (Autohome), Copart or IAAI.

## Quick start

1. Get a demo key in the Telegram bot [@apiautospace_bot](https://t.me/apiautospace_bot?start=demo).
   It is free, needs no card, and works for one day: 100 requests, up to 20 cars per request,
   all three markets and the change feed.
2. Save it: `export APIAUTO_KEY=your-key`.
3. Send the first request:

```bash
curl -s "https://api.apiauto.space/v1/cars?market=kr&brand=Hyundai&model=Grandeur&limit=20" \
  -H "X-API-Key: $APIAUTO_KEY"
```

Python:

```python
import os, httpx

page = httpx.get(
    "https://api.apiauto.space/v1/cars",
    params={"market": "kr", "brand": "Kia", "model": "Sorento", "year_min": 2021, "limit": 20},
    headers={"X-API-Key": os.environ["APIAUTO_KEY"]},
).raise_for_status().json()

for car in page["items"]:
    print(car["title"], car["mileage_km"], car["price"]["amount"], car["price"]["currency"])
```

JavaScript (Node.js 18+):

```js
const response = await fetch("https://api.apiauto.space/v1/cars?market=cn&brand=BYD&limit=20", {
  headers: { "X-API-Key": process.env.APIAUTO_KEY },
});
const { items } = await response.json();
console.log(items.map((car) => `${car.title} · $${car.price_usd}`));
```

Markets: `kr` = Encar, `cn` = Che168, `us` = Copart and IAAI. Call the API from your server: CORS
is off, because a key in browser code is visible to everyone.

## Examples

| Task | curl | Python | JavaScript | PHP |
|---|---|---|---|---|
| First request: search by make, model, year, price | [curl](https://github.com/apiauto-space/encar-api-examples/blob/main/curl/README.md#cars) | [first_request.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/first_request.py) | [first-request.mjs](https://github.com/apiauto-space/encar-api-examples/blob/main/javascript/first-request.mjs) | [first-request.php](https://github.com/apiauto-space/encar-api-examples/blob/main/php/first-request.php) |
| Walk every page with the cursor | [curl](https://github.com/apiauto-space/encar-api-examples/blob/main/curl/README.md#cars) | [sync_catalog.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/sync_catalog.py) | [all-pages.mjs](https://github.com/apiauto-space/encar-api-examples/blob/main/javascript/all-pages.mjs) | [sync-catalog.php](https://github.com/apiauto-space/encar-api-examples/blob/main/php/sync-catalog.php) |
| One model in Korea, China and the USA, prices in dollars | | [compare_markets.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/compare_markets.py) | | |
| Copart and IAAI lots: damage, title, auction date | [curl](https://github.com/apiauto-space/encar-api-examples/blob/main/curl/README.md#cars) | | [us-auctions.mjs](https://github.com/apiauto-space/encar-api-examples/blob/main/javascript/us-auctions.mjs) | |
| Keep a catalog in sync: import plus hourly change feed | [curl](https://github.com/apiauto-space/encar-api-examples/blob/main/curl/README.md#change-feed-new-cars-sold-cars-price-changes) | [sync_catalog.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/sync_catalog.py) | | [sync-catalog.php](https://github.com/apiauto-space/encar-api-examples/blob/main/php/sync-catalog.php) |
| Price drops of 5% or more in 24 hours | [curl](https://github.com/apiauto-space/encar-api-examples/blob/main/curl/README.md#change-feed-new-cars-sold-cars-price-changes) | [price_drops.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/price_drops.py) | [price-drops.mjs](https://github.com/apiauto-space/encar-api-examples/blob/main/javascript/price-drops.mjs) | |
| Export a selection to CSV (Excel, Google Sheets) | | [export_csv.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/export_csv.py) | | |
| Download a car's photos | | [download_photos.py](https://github.com/apiauto-space/encar-api-examples/blob/main/python/download_photos.py) | | |

Real answers of the API are in [samples](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/encar-car.json):

| File | What it contains |
|---|---|
| [encar-car.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/encar-car.json) | An Encar car |
| [che168-car.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/che168-car.json) | A Che168 car |
| [copart-car.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/copart-car.json) | A Copart lot |
| [cars-page-kr.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/cars-page-kr.json) | A page of results |
| [changes-page.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/changes-page.json) | Change feed events |
| [brands-cn.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/brands-cn.json) | Makes in China |
| [models-kr-kia.json](https://github.com/apiauto-space/encar-api-examples/blob/main/samples/models-kr-kia.json) | Kia models in Korea |

## One record format for Encar, Che168, Copart and IAAI

A real Encar car (`GET /v1/cars/encar:43020826`, shortened). Korean source values such as `현대`
and `더 뉴 그랜저 IG` become `Hyundai` and `Grandeur` with generation `The New Grandeur IG`. The
original spellings stay in `raw.source_values`.

```json
{
  "id": "encar:43020826",
  "market": "kr",
  "source": "encar",
  "title": "2020 Hyundai The New Grandeur IG 2.5 Exclusive",
  "brand": "Hyundai",
  "model": "Grandeur",
  "generation": "The New Grandeur IG",
  "trim": "2.5 Exclusive",
  "year": 2020,
  "mileage_km": 82489,
  "fuel": "gasoline",
  "vin": null,
  "price": { "amount": "21600000.00", "currency": "KRW" },
  "price_usd": "16298.48",
  "location": { "country": "KR", "region": "Jeonbuk", "city": null },
  "photos": ["https://api.apiauto.space/img/encar:43020826/1.jpg?exp=…&sig=…"],
  "photo_count": 4,
  "listing_url": "https://fem.encar.com/cars/detail/43020826",
  "is_active": true,
  "first_seen_at": "2026-10-26T04:37:32Z",
  "raw": {
    "condition": ["Inspection", "Record", "Resume"],
    "source_values": { "brand": "현대", "model": "더 뉴 그랜저 IG", "fuel": "가솔린" }
  }
}
```

| Field | Meaning |
|---|---|
| `id` | `source:source_id`, stable: `encar:…`, `che168:…`, `copart:…`, `iaai:…` |
| `brand`, `model` | Latin script, one spelling in every market (`Mercedes-Benz` `E-Class`, `BMW` `3 Series`) |
| `generation` | Korea only: Encar's generation and facelift name |
| `trim` | Encar's badge, Che168's full name, the US variant (`C 300`, `328i`) |
| `year`, `mileage_km`, `engine_cc` | numbers; mileage in kilometres, US miles converted |
| `fuel`, `transmission`, `body_type`, `color` | canonical English values, list in `/v1/references/dictionaries` |
| `price`, `price_usd` | price in KRW / CNY / USD and in dollars at the ECB daily rate |
| `photos`, `photo_count` | signed photo links, valid about a day: keep the id, not the link |
| `is_active`, `first_seen_at`, `disappeared_at` | status: a sold car stays 14 days with `is_active: false` |
| `raw` | source-only fields: Encar inspection marks, Che168 power and drive, Copart and IAAI damage, title, auction date |

What the source does not give is `null`, never a guess. Full schema: [openapi.json](https://api.apiauto.space/openapi.json),
[Swagger UI](https://api.apiauto.space/docs/swagger), [the record](https://apiauto.space/en/docs/record/).

## Markets

On 27 October 2026 the catalog held about 140,000 cars from Encar, 234,000 from Che168 and
80,000 upcoming Copart and IAAI lots. Live numbers are in `GET /v1/references/markets`.

| Market | Source | Refresh | VIN | Not in the source |
|---|---|---|---|---|
| `kr` | [Encar](https://apiauto.space/en/encar-api/) | hourly by target | rare (~0.1%) | gearbox, engine size |
| `cn` | [Che168](https://apiauto.space/en/che168-api/) | hourly by target | no | VIN |
| `us` | [Copart](https://apiauto.space/en/copart-api/), [IAAI](https://apiauto.space/en/iaai-api/) | hourly by target | yes | past auctions, final prices of old lots |

Every answer carries `X-Data-Age-Seconds`, the real age of the market copy.

## Endpoints

| Request | What it does | Quota |
|---|---|---|
| `GET /v1/cars` | Catalog of a market: filters, sort, cursor, up to 100 cars a page | 1 record per car |
| `GET /v1/cars/{id}` | One car, including cars taken off sale in the last 14 days | 1 record |
| `GET /v1/changes` | New cars, removed cars, price drops and rises since a moment | 1 record per event |
| `GET /v1/references/brands`, `models`, `dictionaries`, `markets` | Spellings, filter values, freshness | free |
| `GET /v1/usage` | Plan and quota | free |
| `GET /v1/us/live` | Live Copart and IAAI search beyond the copy (Pro, Max) | own counter |

Quota counts cars, not requests: an answer with 37 cars costs 37 records, an empty one costs
nothing. Plans: Start $59 a month (1 market, 100,000 cars), Pro $149 (2 markets, 500,000 cars,
change feed), Max $299 (3 markets, 2,000,000 cars), [details](https://apiauto.space/en/#pricing).

## Client libraries

| Language | Package | Repository |
|---|---|---|
| Python | `pip install apiauto` | [apiauto-space/apiauto-python](https://github.com/apiauto-space/apiauto-python) |
| JavaScript / TypeScript | `npm i apiauto` | [apiauto-space/apiauto-js](https://github.com/apiauto-space/apiauto-js) |
| Any language | [openapi.json](https://api.apiauto.space/openapi.json) | generate a client with openapi-generator |

## FAQ

**Does Encar have an official API?** No. Encar has no public API for listings: its site works on
internal endpoints that block automated traffic. apiauto.space gives Encar listings through a
documented API with a key.

**Is this an Encar parser?** It is a ready API instead of a parser of your own. You don't maintain
scrapers, proxies and captcha workarounds, and you don't chase layout changes. You get JSON, a
cursor and a change feed.

**Che168 has no VIN?** Right, Che168 listings do not publish VINs, so `vin` is `null` for China.
Korea has a VIN on about 0.1% of cars; Copart and IAAI lots have VINs.

**How do I know a car was sold?** Listings do not say "sold". A car that leaves the source gets
`is_active: false` and a `disappeared` event in `/v1/changes`; recheck a car by id right before a
purchase.

**Can I call the API from a browser?** No, only from a server: CORS is off so the key stays
private.

## По-русски

Примеры работы с API [apiauto.space](https://apiauto.space/): объявления с **Encar**
(Южная Корея), **Che168** (Китай) и аукционов **Copart** и **IAAI** (США) в одном формате JSON.
Это готовый API вместо собственного парсера Encar или Che168: не нужно держать прокси, обходить
капчи и чинить парсер после каждого изменения вёрстки. Марки и модели приходят латиницей в одном
написании для всех стран, цены — в валюте рынка и в долларах по курсу ЕЦБ. Есть лента изменений:
новые, снятые и подешевевшие машины. Бесплатный тестовый ключ на сутки (100 запросов) выдаёт
Telegram-бот [@apiautospace_bot](https://t.me/apiautospace_bot?start=demo).
Документация на русском: [apiauto.space/docs/](https://apiauto.space/docs/).

```bash
curl -s "https://api.apiauto.space/v1/cars?market=kr&brand=Kia&model=Carnival&limit=20" \
  -H "X-API-Key: $APIAUTO_KEY"
```

## License and disclaimer

The examples are MIT-licensed: copy them into your project.
Encar, Che168, Autohome, Copart and IAAI are trademarks of their owners; apiauto.space is not
affiliated with them. Listing data and photos belong to the sources and sellers.
