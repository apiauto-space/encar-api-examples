// Walk every page of a selection with the cursor, as an async generator.
//
//   export APIAUTO_KEY=...
//   node all-pages.mjs
//
// Every car returned is one record of quota, so stop when you have enough.

const BASE = "https://api.apiauto.space/v1";

async function* cars(filters, { maxItems = Infinity } = {}) {
  const params = new URLSearchParams({ limit: "20", ...filters });
  let yielded = 0;
  while (true) {
    const response = await fetch(`${BASE}/cars?${params}`, {
      headers: { "X-API-Key": process.env.APIAUTO_KEY },
    });
    if (response.status === 429) {
      // Rate limit: wait as long as the API asks, then retry the same page.
      const seconds = Number(response.headers.get("Retry-After") ?? 1);
      await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
      continue;
    }
    if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`);

    const page = await response.json();
    for (const car of page.items) {
      if (yielded++ >= maxItems) return;
      yield car;
    }
    if (!page.next_cursor) return;
    params.set("cursor", page.next_cursor);
  }
}

// Korean Kia Carnivals from 2021 with under 60,000 km, the first 60 of them.
for await (const car of cars(
  { market: "kr", brand: "Kia", model: "Carnival", year_min: "2021", mileage_max: "60000" },
  { maxItems: 60 },
)) {
  console.log(car.id, car.title, car.mileage_km, car.price_usd);
}
