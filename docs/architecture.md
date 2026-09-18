# Architecture & Design Notes

## Data Layers

| Layer | Purpose |
|---|---|
| Landing | Immutable daily CSV batches |
| Rejected | Invalid records with rejection reason |
| Raw warehouse | Accepted records plus source and load metadata |
| Staging | Typed, standardized, reusable dbt view |
| Marts | Business-ready daily, category, and customer tables |
| Presentation | Streamlit dashboard |

## Reliability Controls

- Deterministic daily source generation
- Required-column validation
- Row-level domain checks
- Duplicate detection inside a file
- File hashing and load audit
- Business-key upserts
- Transactional database writes
- Airflow retries and single active run
- dbt uniqueness, not-null, and accepted-value tests
- pytest coverage for generator, validator, loader, and model contracts

## Idempotency

Two layers provide idempotency:

1. A file hash prevents the exact same batch from loading twice.
2. `order_id` upserts prevent duplicated business entities when corrected files arrive.

## Production Evolution

A production version could add object storage, schema registry, secrets management, managed PostgreSQL, observability, alert routing, data lineage, CDC, and a streaming path. These capabilities are future scope, not claims of the portfolio implementation.

