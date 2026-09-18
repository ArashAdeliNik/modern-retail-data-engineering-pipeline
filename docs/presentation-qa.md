# Presentation Questions & Answers

## Why use both Airflow and dbt?

Airflow coordinates when tasks run and how failures are retried. dbt owns SQL transformations, dependencies, documentation, and warehouse tests.

## How is duplicate loading prevented?

The loader tracks each source file by SHA-256 hash and skips previously loaded files. It also upserts on `order_id`.

## What happens to invalid records?

They are excluded from the raw warehouse and written to a rejected-data file with an explicit reason.

## Why PostgreSQL?

It provides a realistic relational warehouse for the portfolio scale, supports transactional upserts, and integrates well with Airflow, dbt, SQLAlchemy, and Streamlit.

## Why is SQLite included?

SQLite is a lightweight test path for the core loader. It keeps automated tests fast while the full Docker stack uses PostgreSQL.

## Is this streaming?

No. It is a daily batch pipeline. Streaming would be justified only by a lower-latency business requirement.

## What did you test?

Deterministic generation, quality-rule behavior, duplicate rejection, file idempotency, database row counts, expected dbt model presence, Python linting, and dbt warehouse tests.

## What would change in production?

Secrets management, managed storage and database, monitoring, alerting, backup policy, access control, capacity planning, and infrastructure-as-code would be added.

