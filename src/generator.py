from __future__ import annotations

import csv
import random
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

CATEGORIES = {
    "electronics": (35.0, 900.0),
    "home": (8.0, 240.0),
    "beauty": (4.0, 120.0),
    "sports": (10.0, 300.0),
    "books": (3.0, 55.0),
}
CITIES = ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"]
PAYMENTS = ["card", "wallet", "bank_transfer"]
STATUSES = ["completed", "completed", "completed", "refunded", "cancelled"]
FIELDS = [
    "order_id", "order_timestamp", "customer_id", "product_id", "category",
    "quantity", "unit_price", "discount_pct", "payment_method", "city",
    "order_status", "updated_at",
]


def generate_orders(output_dir: Path, run_date: date, rows: int = 500, seed: int = 42) -> Path:
    """Generate a deterministic daily retail order file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(f"{seed}-{run_date.isoformat()}")
    path = output_dir / f"orders_{run_date.isoformat()}.csv"
    start = datetime.combine(run_date, datetime.min.time(), tzinfo=UTC)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for index in range(rows):
            category = rng.choice(list(CATEGORIES))
            low, high = CATEGORIES[category]
            order_time = start + timedelta(seconds=rng.randint(0, 86_399))
            writer.writerow(
                {
                    "order_id": f"ORD-{run_date:%Y%m%d}-{index + 1:06d}",
                    "order_timestamp": order_time.isoformat(),
                    "customer_id": f"CUS-{rng.randint(1, 1800):05d}",
                    "product_id": f"PRD-{category[:3].upper()}-{rng.randint(1, 150):04d}",
                    "category": category,
                    "quantity": rng.randint(1, 5),
                    "unit_price": round(rng.uniform(low, high), 2),
                    "discount_pct": rng.choice([0, 0, 0.05, 0.10, 0.15, 0.20]),
                    "payment_method": rng.choice(PAYMENTS),
                    "city": rng.choice(CITIES),
                    "order_status": rng.choice(STATUSES),
                    "updated_at": datetime.now(UTC).isoformat(),
                }
            )
    return path

