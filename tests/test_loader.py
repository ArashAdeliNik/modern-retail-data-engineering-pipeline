from datetime import date

from sqlalchemy import create_engine, text

from src.generator import generate_orders
from src.loader import ingest_file


def test_ingestion_is_idempotent(tmp_path):
    source = generate_orders(tmp_path / "landing", date(2026, 9, 18), rows=25)
    database_url = f"sqlite:///{tmp_path / 'warehouse.db'}"
    first = ingest_file(source, database_url, tmp_path / "rejected")
    second = ingest_file(source, database_url, tmp_path / "rejected")

    assert first["accepted"] == 25
    assert first["skipped"] is False
    assert second["skipped"] is True

    engine = create_engine(database_url)
    with engine.begin() as connection:
        count = connection.execute(text("select count(*) from raw_orders")).scalar_one()
    assert count == 25

