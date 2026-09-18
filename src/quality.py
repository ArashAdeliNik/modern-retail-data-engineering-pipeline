from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {
    "order_id", "order_timestamp", "customer_id", "product_id", "category",
    "quantity", "unit_price", "discount_pct", "payment_method", "city",
    "order_status", "updated_at",
}
ALLOWED_STATUSES = {"completed", "refunded", "cancelled"}


def validate_orders(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a batch into accepted and rejected records with rejection reasons."""
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    checked = frame.copy()
    reasons = pd.Series("", index=checked.index, dtype="object")

    def flag(mask: pd.Series, message: str) -> None:
        nonlocal reasons
        reasons = reasons.mask(mask & reasons.eq(""), message)

    flag(checked["order_id"].isna() | checked["order_id"].astype(str).str.strip().eq(""), "missing_order_id")
    flag(checked["order_id"].duplicated(keep=False), "duplicate_order_id_in_file")
    flag(pd.to_numeric(checked["quantity"], errors="coerce").le(0), "invalid_quantity")
    flag(pd.to_numeric(checked["unit_price"], errors="coerce").lt(0), "invalid_unit_price")
    discount = pd.to_numeric(checked["discount_pct"], errors="coerce")
    flag(discount.lt(0) | discount.gt(0.70), "invalid_discount")
    flag(~checked["order_status"].isin(ALLOWED_STATUSES), "invalid_status")
    parsed_time = pd.to_datetime(checked["order_timestamp"], errors="coerce", utc=True)
    flag(parsed_time.isna(), "invalid_timestamp")

    rejected = checked.loc[reasons.ne("")].copy()
    rejected["rejection_reason"] = reasons.loc[reasons.ne("")]
    accepted = checked.loc[reasons.eq("")].copy()
    return accepted, rejected

