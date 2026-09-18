from datetime import date

import pandas as pd

from src.generator import generate_orders


def test_generator_is_deterministic(tmp_path):
    path = generate_orders(tmp_path, date(2026, 9, 18), rows=20, seed=7)
    first = pd.read_csv(path)
    path = generate_orders(tmp_path, date(2026, 9, 18), rows=20, seed=7)
    second = pd.read_csv(path)
    pd.testing.assert_frame_equal(first.drop(columns=["updated_at"]), second.drop(columns=["updated_at"]))
    assert len(first) == 20
    assert first["order_id"].is_unique

