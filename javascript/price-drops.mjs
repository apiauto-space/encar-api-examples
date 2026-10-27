// Cars whose price dropped by 5% or more in the last 24 hours.
//
//   export APIAUTO_KEY=...
//   node price-drops.mjs kr
//
// The change feed (/v1/changes) comes with Pro, Max and the demo key.

const market = process.argv[2] ?? "kr";
const headers = { "X-API-Key": process.env.APIAUTO_KEY };
const BASE = "https://api.apiauto.space/v1";

async function get(path, params = {}) {
  const query = new URLSearchParams(params).toString();
  const response = await fetch(`${BASE}${path}${query ? `?${query}` : ""}`, { headers });
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`);
  return response.json();
}

const since = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
const { items: events } = await get("/changes", {
  market,
  since,
  type: "price_drop",
  min_pct: "5",
  limit: "10",
});

if (events.length === 0) console.log("No price drops of 5% or more in the last 24 hours");
for (const event of events) {
  const car = await get(`/cars/${event.car_id}`);
  console.log(
    `-${Number(event.pct).toFixed(1)}%  ${car.title}: ` +
      `${event.old_price} → ${event.new_price} ${car.price.currency}  ${car.listing_url ?? car.id}`,
  );
}
