// Search Che168 (China) by make and price and print the cars.
//
//   export APIAUTO_KEY=...   # the demo key from https://t.me/apiautospace_bot?start=demo
//   node first-request.mjs   # Node 18+, no dependencies
//
// Call the API from your server: CORS is off, and a key in browser code is public.

const params = new URLSearchParams({
  market: "cn", // kr = Encar, cn = Che168, us = Copart and IAAI
  brand: "BYD",
  price_usd_max: "20000", // dollars at the ECB daily rate
  sort: "-first_seen", // newest listings first
  limit: "20", // up to 20 on the demo key, up to 100 on paid plans
});

const response = await fetch(`https://api.apiauto.space/v1/cars?${params}`, {
  headers: { "X-API-Key": process.env.APIAUTO_KEY },
});
if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`);

const { items, count } = await response.json();
console.log(`${count ?? "10,000+"} cars match, showing ${items.length}`);
for (const car of items) {
  console.log(
    `${car.id.padEnd(18)} ${car.title.padEnd(40)} ${car.mileage_km ?? "?"} km  ` +
      `${car.price.amount} ${car.price.currency} (≈ $${car.price_usd})`,
  );
}

console.log("records left:", response.headers.get("X-Quota-Remaining"));
console.log("data age, s:", response.headers.get("X-Data-Age-Seconds"));
