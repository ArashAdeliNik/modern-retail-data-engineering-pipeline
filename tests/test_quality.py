import pandas as pd

from src.quality import validate_orders


def valid_row():
    return {
        "order_id": "ORD-1",
        "order_timestamp": "2026-09-18T10:00:00+00:00",
        "customer_id": "CUS-1",
        "product_id": "PRD-1",
        "category": "books",
        "quantity": 2,
        "unit_price": 12.5,
        "discount_pct": 0.1,
        "payment_method": "card",
        "city": "Berlin",
        "order_status": "completed",
        "updated_at": "2026-09-18T10:00:00+00:00",
    }


def test_quality_splits_valid_and_invalid_rows():
    good = valid_row()
    bad = {**valid_row(), "order_id": "ORD-2", "quantity": 0}
    accepted, rejected = validate_orders(pd.DataFrame([good, bad]))
    assert accepted["order_id"].tolist() == ["ORD-1"]
    assert rejected.iloc[0]["rejection_reason"] == "invalid_quantity"


def test_quality_rejects_duplicate_ids():
    accepted, rejected = validate_orders(pd.DataFrame([valid_row(), valid_row()]))
    assert accepted.empty
    assert len(rejected) == 2

