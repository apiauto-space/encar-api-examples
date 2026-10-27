<?php
// Search Encar (South Korea) and print the cars. PHP 7.4+ with the curl extension.
//
//   export APIAUTO_KEY=...   # the demo key from https://t.me/apiautospace_bot?start=demo
//   php first-request.php

function apiauto_get(string $path, array $params = []): array
{
    $url = "https://api.apiauto.space/v1" . $path . ($params ? "?" . http_build_query($params) : "");
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_HTTPHEADER => ["X-API-Key: " . getenv("APIAUTO_KEY")],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
    ]);
    $body = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    if ($status !== 200) {
        // Errors are JSON too: {"error": "quota_exhausted", "reset_at": "..."}
        throw new RuntimeException("HTTP $status: $body");
    }
    return json_decode($body, true);
}

$page = apiauto_get("/cars", [
    "market" => "kr",         // kr = Encar, cn = Che168, us = Copart and IAAI
    "brand" => "Kia",
    "model" => "Sorento",
    "year_min" => 2021,
    "price_usd_min" => 5000,  // skips leases that Encar lists with a monthly payment
    "limit" => 20,            // up to 20 on the demo key, up to 100 on paid plans
]);

printf("%s cars match\n", $page["count"] ?? "10,000+");
foreach ($page["items"] as $car) {
    printf(
        "%-18s %-45s %7s km  %s %s (≈ $%s)\n",
        $car["id"],
        $car["title"],
        $car["mileage_km"] ?? "?",
        $car["price"]["amount"],
        $car["price"]["currency"],
        $car["price_usd"]
    );
}
