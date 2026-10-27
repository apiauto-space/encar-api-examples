# Encar, Che168, Copart and IAAI API with curl

Every request of the [apiauto.space API](https://apiauto.space/en/docs/) from the command line.
Put the key in a variable first; the demo key comes from
[the Telegram bot](https://t.me/apiautospace_bot?start=demo) (one day, 100 requests).

```bash
export APIAUTO_KEY=your-key
API=https://api.apiauto.space/v1
```

Add `| jq` to any command for readable JSON, `-i` to see the quota headers.

## Cars

```bash
# Encar (South Korea): Hyundai Grandeur from 2020, cheapest first
curl -s "$API/cars?market=kr&brand=Hyundai&model=Grandeur&year_min=2020&sort=price&limit=20" \
  -H "X-API-Key: $APIAUTO_KEY"

# Che168 (China): BYD under $20,000, newest listings first
curl -s "$API/cars?market=cn&brand=BYD&price_usd_max=20000&limit=20" \
  -H "X-API-Key: $APIAUTO_KEY"

# Copart and IAAI (USA): 2020+ Toyota RAV4 lots with photos
curl -s "$API/cars?market=us&brand=Toyota&model=RAV4&year_min=2020&has_photos=true&limit=20" \
  -H "X-API-Key: $APIAUTO_KEY"

# Free text: up to 6 words of the title
curl -s "$API/cars?market=kr&q=2021+Genesis+GV80&limit=20" -H "X-API-Key: $APIAUTO_KEY"

# The next page: pass next_cursor of the previous answer
curl -s "$API/cars?market=kr&brand=Kia&limit=20&cursor=PASTE_NEXT_CURSOR" \
  -H "X-API-Key: $APIAUTO_KEY"
```

Filters: `brand`, `model`, `generation` (Korea), `trim`, `year_min`, `year_max`,
`price_min`, `price_max` (market currency), `price_usd_min`, `price_usd_max`, `mileage_max` (km),
`fuel`, `transmission`, `body_type`, `has_photos`, `is_active`, `q`. Sort: `-first_seen`
(default), `first_seen`, `price`, `-price`, `year`, `-year`, `mileage`, `-mileage`.

## One car

```bash
curl -s "$API/cars/encar:43020826" -H "X-API-Key: $APIAUTO_KEY"
curl -s "$API/cars/che168:60325801" -H "X-API-Key: $APIAUTO_KEY"
curl -s "$API/cars/copart:73450206" -H "X-API-Key: $APIAUTO_KEY"
```

A car taken off sale answers with `is_active: false` for 14 more days, then 404.

## Change feed: new cars, sold cars, price changes

```bash
# Everything that happened in Korea since a moment
curl -s "$API/changes?market=kr&since=2026-10-27T00:00:00Z&limit=100" -H "X-API-Key: $APIAUTO_KEY"

# Only price drops of 5% or more in China
curl -s "$API/changes?market=cn&since=2026-10-27T00:00:00Z&type=price_drop&min_pct=5" \
  -H "X-API-Key: $APIAUTO_KEY"
```

Event types: `added`, `disappeared` (sold or withdrawn), `price_drop`, `price_up`.

## References (free, no quota)

```bash
curl -s "$API/references/brands?market=cn" -H "X-API-Key: $APIAUTO_KEY"
curl -s "$API/references/models?market=kr&brand=Kia" -H "X-API-Key: $APIAUTO_KEY"
curl -s "$API/references/dictionaries" -H "X-API-Key: $APIAUTO_KEY"   # fuel, gearbox, body…
curl -s "$API/references/markets" -H "X-API-Key: $APIAUTO_KEY"        # freshness and counts
curl -s "$API/usage" -H "X-API-Key: $APIAUTO_KEY"                     # your quota
```

## Live US search (Pro and Max)

```bash
curl -s "$API/us/live?make=Toyota&model=Camry&year_min=2020" -H "X-API-Key: $APIAUTO_KEY"
```

## Quota headers

```bash
curl -si "$API/cars?market=kr&limit=1" -H "X-API-Key: $APIAUTO_KEY" | grep -i '^x-'
```

```
X-Quota-Limit: 100
X-Quota-Remaining: 97
X-Quota-Reset: 2026-10-28T12:04:00Z
X-RateLimit-Limit: 1
X-Data-Age-Seconds: 938
```

Errors are JSON: `{"error": "rate_limited", "retry_after": 1}`; the codes are on
[apiauto.space/en/docs/errors/](https://apiauto.space/en/docs/errors/).
