# Data Quality Rules

| Rule | Action on failure |
|---|---|
| Required columns exist | Fail the batch with a clear error |
| `order_id` is present | Reject row |
| `order_id` is unique within file | Reject duplicates |
| Quantity is greater than zero | Reject row |
| Unit price is non-negative | Reject row |
| Discount is between 0 and 0.70 | Reject row |
| Status belongs to approved domain | Reject row |
| Timestamp parses as UTC time | Reject row |

Rejected rows remain outside the warehouse and include a `rejection_reason` column. dbt tests then verify warehouse and mart contracts after transformation.

