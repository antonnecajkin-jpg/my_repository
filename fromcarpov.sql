select 
    temp.date,
    temp.orders_count,
    round(avg(temp.orders_count) over(order by temp.date ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING), 2) as moving_avg

from(select creation_time::date as date, count(*) as orders_count
from orders
where order_id not in(
    select order_id
    from user_actions
    where action = 'cancel_order'

)
group by date) as temp


;) t