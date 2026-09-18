from __future__ import annotations

import argparse
import json
from datetime import UTC, date, datetime

from src.config import DATABASE_URL, LANDING_DIR, REJECTED_DIR
from src.generator import generate_orders
from src.loader import ingest_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic retail data pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate")
    today = datetime.now(UTC).date().isoformat()
    generate.add_argument("--date", default=today)
    generate.add_argument("--rows", type=int, default=500)
    generate.add_argument("--seed", type=int, default=42)
    sub.add_parser("ingest")
    all_steps = sub.add_parser("all")
    all_steps.add_argument("--date", default=today)
    all_steps.add_argument("--rows", type=int, default=500)

    args = parser.parse_args()
    if args.command in {"generate", "all"}:
        path = generate_orders(LANDING_DIR, date.fromisoformat(args.date), args.rows, getattr(args, "seed", 42))
        print(json.dumps({"generated": str(path)}))
    if args.command in {"ingest", "all"}:
        print(json.dumps(ingest_directory(LANDING_DIR, DATABASE_URL, REJECTED_DIR), default=str))


if __name__ == "__main__":
    main()
