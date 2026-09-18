from pathlib import Path


def test_expected_dbt_models_exist():
    root = Path(__file__).resolve().parents[1] / "dbt" / "models"
    expected = {
        root / "staging" / "stg_orders.sql",
        root / "marts" / "mart_daily_sales.sql",
        root / "marts" / "mart_category_performance.sql",
        root / "marts" / "mart_customer_summary.sql",
    }
    assert all(path.exists() for path in expected)

