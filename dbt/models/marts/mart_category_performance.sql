select
    category,
    count(*) filter (where order_status = 'completed') as completed_orders,
    round(sum(case when order_status = 'completed' then gross_revenue else 0 end), 2) as net_revenue,
    sum(case when order_status = 'completed' then quantity else 0 end) as units_sold,
    round(avg(discount_pct), 4) as average_discount
from {{ ref('stg_orders') }}
group by 1

