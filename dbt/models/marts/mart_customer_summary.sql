select
    customer_id,
    min(order_date) as first_order_date,
    max(order_date) as last_order_date,
    count(*) filter (where order_status = 'completed') as completed_orders,
    round(sum(case when order_status = 'completed' then gross_revenue else 0 end), 2) as lifetime_value,
    count(distinct category) as categories_purchased
from {{ ref('stg_orders') }}
group by 1

