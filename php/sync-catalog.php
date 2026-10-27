<?php
// Keep a catalog in MySQL/PostgreSQL in sync: import once, then poll the change feed hourly.
// Run it from cron: `0 * * * * php sync-catalog.php`. PHP 7.4+ with curl.
//
// The SQL is left as comments: plug in your own database layer.

const API = "https://api.apiauto.space/v1";
const MARKET = "kr";
const STATE_FILE = __DIR__ . "/since.txt";

function apiauto_get(string $path, array $params = []): array
{
    while (true) {
        $ch = curl_init(API . $path . ($params ? "?" . http_build_query($params) : ""));
        curl_setopt_array($ch, [
            CURLOPT_HTTPHEADER => ["X-API-Key: " . getenv("APIAUTO_KEY")],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => true,
            CURLOPT_TIMEOUT => 60,
        ]);
        $response = curl_exec($ch);
        $status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        curl_close($ch);
        $body = substr($response, $headerSize);

        if ($status === 429 || $status === 503) {
            // Wait as long as the API asks (Retry-After), then repeat the request.
            preg_match('/^retry-after:\s*(\d+)/mi', substr($response, 0, $headerSize), $m);
            sleep((int)($m[1] ?? 1));
            continue;
        }
        if ($status !== 200) {
            throw new RuntimeException("HTTP $status: $body");
        }
        return json_decode($body, true);
    }
}

function save_car(array $car): void
{
    // INSERT ... ON CONFLICT (id) DO UPDATE: id, title, price.amount, price.currency, price_usd,
    // mileage_km, photos (refresh them when showing the car: links live about a day), raw.
    echo "save {$car['id']} {$car['title']}\n";
}

if (!file_exists(STATE_FILE)) {
    // The first run: the whole selection by the cursor.
    $since = gmdate("Y-m-d\TH:i:s\Z");
    $params = ["market" => MARKET, "brand" => "Hyundai", "limit" => 100]; // 20 on the demo key
    do {
        $page = apiauto_get("/cars", $params);
        array_map("save_car", $page["items"]);
        $params["cursor"] = $page["next_cursor"];
    } while ($page["next_cursor"]);
} else {
    // Every next run: only what changed since the last one.
    $since = trim(file_get_contents(STATE_FILE));
    $now = gmdate("Y-m-d\TH:i:s\Z");
    $params = ["market" => MARKET, "since" => $since, "limit" => 100];  // 20 on the demo key
    do {
        $page = apiauto_get("/changes", $params);
        foreach ($page["items"] as $event) {
            switch ($event["type"]) {
                case "added":
                    save_car(apiauto_get("/cars/" . $event["car_id"]));
                    break;
                case "disappeared": // sold or withdrawn
                    // UPDATE cars SET is_active = false WHERE id = $event["car_id"]
                    echo "sold {$event['car_id']}\n";
                    break;
                default: // price_drop, price_up
                    // UPDATE cars SET price = $event["new_price"] WHERE id = $event["car_id"]
                    echo "{$event['type']} {$event['car_id']}: {$event['old_price']} → {$event['new_price']}\n";
            }
        }
        $params["cursor"] = $page["next_cursor"];
    } while ($page["next_cursor"]);
    $since = $now;
}

file_put_contents(STATE_FILE, $since);
