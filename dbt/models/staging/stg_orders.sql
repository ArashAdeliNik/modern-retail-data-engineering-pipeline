select
    order_id,
    cast(order_timestamp as timestamp) as order_timestamp,
    cast(order_timestamp as date) as order_date,
    customer_id,
    product_id,
    lower(category) as category,
    cast(quantity as integer) as quantity,
    cast(unit_price as numeric(12, 2)) as unit_price,
    cast(discount_pct as numeric(6, 4)) as discount_pct,
    lower(payment_method) as payment_method,
    city,
    lower(order_status) as order_status,
    round((quantity * unit_price * (1 - discount_pct))::numeric, 2) as gross_revenue,
    source_file,
    loaded_at
from {{ source('raw', 'raw_orders') }}

