# Five-Minute Demo Script

## 0:00–0:40 — Goal

Explain that the project demonstrates a dependable batch pipeline rather than a single analysis notebook.

## 0:40–1:20 — Source and Validation

Generate a synthetic daily order file. Show the contract and explain that invalid rows are quarantined with reasons.

## 1:20–2:10 — Incremental Loading

Run ingestion twice. The first run loads records; the second skips the same file hash. Explain business-key upserts.

## 2:10–3:00 — Airflow

Open the DAG and show generation, ingestion, dbt transformation, and dbt testing as separate observable tasks.

## 3:00–3:50 — dbt

Show the staging model, three marts, and schema tests. Explain why dashboard queries do not read raw files.

## 3:50–4:40 — Dashboard

Show daily revenue, completed orders, customer count, average order value, trend, and category performance.

## 4:40–5:00 — Close

Summarize idempotency, auditability, data quality, orchestration, and containerized reproducibility.

