select
    order_date,
    count(*) as total_orders,
    count(*) filter (where order_status = 'completed') as completed_orders,
    count(*) filter (where order_status = 'refunded') as refunded_orders,
    count(*) filter (where order_status = 'cancelled') as cancelled_orders,
    round(sum(case when order_status = 'completed' then gross_revenue else 0 end), 2) as net_revenue,
    count(distinct customer_id) as unique_customers,
    round(avg(case when order_status = 'completed' then gross_revenue end), 2) as average_order_value
from {{ ref('stg_orders') }}
group by 1

