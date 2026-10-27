// Upcoming Copart and IAAI lots: damage, title document, auction date and buy-now price.
//
//   export APIAUTO_KEY=...
//   node us-auctions.mjs Toyota RAV4
//
// The US market holds lots whose auction is still ahead; a sold lot leaves the catalog
// (is_active=false) and stays reachable by id for 14 days.

const [brand = "Toyota", model = "RAV4"] = process.argv.slice(2);
const params = new URLSearchParams({
  market: "us",
  brand,
  model,
  year_min: "2020",
  has_photos: "true",
  limit: "20",
});

const response = await fetch(`https://api.apiauto.space/v1/cars?${params}`, {
  headers: { "X-API-Key": process.env.APIAUTO_KEY },
});
if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`);

const { items } = await response.json();
for (const car of items) {
  const { raw } = car; // source-only fields: auction, damage, title, odometer in miles
  console.log(
    [
      `${car.source}:${raw.lot_number}`,
      car.title,
      `VIN ${car.vin ?? "—"}`,
      `damage: ${raw.damage_main ?? "—"}`,
      `title: ${raw.title_doc ?? "—"}`,
      `sale: ${raw.sale_date?.slice(0, 16) ?? "—"}`,
      `buy now: ${raw.buy_now ? `$${raw.buy_now}` : "—"}`,
      `${car.location.city}, ${car.location.region}`,
    ].join(" · "),
  );
}
