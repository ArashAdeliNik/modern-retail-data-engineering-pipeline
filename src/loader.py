from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from src.quality import validate_orders

RAW_DDL = """
CREATE TABLE IF NOT EXISTS raw_orders (
    order_id VARCHAR(64) PRIMARY KEY,
    order_timestamp TIMESTAMP NOT NULL,
    customer_id VARCHAR(64) NOT NULL,
    product_id VARCHAR(64) NOT NULL,
    category VARCHAR(64) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount_pct NUMERIC(6,4) NOT NULL,
    payment_method VARCHAR(32) NOT NULL,
    city VARCHAR(64) NOT NULL,
    order_status VARCHAR(32) NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    source_file VARCHAR(255) NOT NULL,
    loaded_at TIMESTAMP NOT NULL
)
"""
LOG_DDL = """
CREATE TABLE IF NOT EXISTS etl_file_log (
    file_hash VARCHAR(64) PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    accepted_rows INTEGER NOT NULL,
    rejected_rows INTEGER NOT NULL,
    loaded_at TIMESTAMP NOT NULL
)
"""
UPSERT = """
INSERT INTO raw_orders (
    order_id, order_timestamp, customer_id, product_id, category, quantity,
    unit_price, discount_pct, payment_method, city, order_status, updated_at,
    source_file, loaded_at
) VALUES (
    :order_id, :order_timestamp, :customer_id, :product_id, :category, :quantity,
    :unit_price, :discount_pct, :payment_method, :city, :order_status, :updated_at,
    :source_file, :loaded_at
)
ON CONFLICT (order_id) DO UPDATE SET
    order_timestamp = excluded.order_timestamp,
    customer_id = excluded.customer_id,
    product_id = excluded.product_id,
    category = excluded.category,
    quantity = excluded.quantity,
    unit_price = excluded.unit_price,
    discount_pct = excluded.discount_pct,
    payment_method = excluded.payment_method,
    city = excluded.city,
    order_status = excluded.order_status,
    updated_at = excluded.updated_at,
    source_file = excluded.source_file,
    loaded_at = excluded.loaded_at
"""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ingest_file(path: Path, database_url: str, rejected_dir: Path) -> dict[str, int | str | bool]:
    """Validate and idempotently upsert one CSV batch."""
    engine = create_engine(database_url, future=True)
    file_hash = _sha256(path)
    loaded_at = datetime.now(UTC)

    with engine.begin() as connection:
        connection.execute(text(RAW_DDL))
        connection.execute(text(LOG_DDL))
        exists = connection.execute(
            text("SELECT 1 FROM etl_file_log WHERE file_hash = :file_hash"),
            {"file_hash": file_hash},
        ).first()
    if exists:
        return {"file": path.name, "skipped": True, "accepted": 0, "rejected": 0}

    frame = pd.read_csv(path)
    accepted, rejected = validate_orders(frame)
    if not rejected.empty:
        rejected_dir.mkdir(parents=True, exist_ok=True)
        rejected.to_csv(rejected_dir / f"{path.stem}_rejected.csv", index=False)

    records = accepted.to_dict(orient="records")
    for record in records:
        record["source_file"] = path.name
        record["loaded_at"] = loaded_at

    with engine.begin() as connection:
        if records:
            connection.execute(text(UPSERT), records)
        connection.execute(
            text("""
            INSERT INTO etl_file_log (file_hash, file_name, accepted_rows, rejected_rows, loaded_at)
            VALUES (:file_hash, :file_name, :accepted, :rejected, :loaded_at)
            """),
            {
                "file_hash": file_hash,
                "file_name": path.name,
                "accepted": len(accepted),
                "rejected": len(rejected),
                "loaded_at": loaded_at,
            },
        )
    return {"file": path.name, "skipped": False, "accepted": len(accepted), "rejected": len(rejected)}


def ingest_directory(landing_dir: Path, database_url: str, rejected_dir: Path) -> list[dict[str, int | str | bool]]:
    return [ingest_file(path, database_url, rejected_dir) for path in sorted(landing_dir.glob("orders_*.csv"))]

