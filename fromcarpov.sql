select 
    user_id, 
    order_id, 
    time, 
    ROW_NUMBER() over (PARTITION BY user_id ORDER BY order_id) as order_number,
    LAG(time, 1) over (PARTITION by user_id) as time_lag,
    AGE(time, LAG(time, 1) over (PARTITION by user_id)) as time_diff
from user_actions
where order_id not in(
                   select order_id from user_actions
                   where action = 'cancel_order'
                   )
ORDER BY user_id, 
         order_id
LIMIT 1000;