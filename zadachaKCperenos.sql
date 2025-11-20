select 
    temp.user_id, 
    temp.order_id, 
    temp.time, 
    temp.order_number, 
    temp.time_lag, 
    temp.time_diff, 
    temp.counter, 
    SELECT EXTRACT(epoch FROM INTERVAL avg(temp.time_diff) over(partition by temp.user_id)) as hours_between_orders
from (
    SELECT 
        user_id,
        order_id,
        time,
        row_number() OVER (PARTITION BY user_id ORDER BY order_id) as order_number,
       lag(time, 1) OVER (PARTITION BY user_id) as time_lag,
       age(time, lag(time, 1) OVER (PARTITION BY user_id)) as time_diff, 
       count(order_id) over(PARTITION BY user_id) as counter
       
    FROM   user_actions
    WHERE  
        order_id not in(
                        SELECT order_id
                        FROM   user_actions
                        WHERE  action = 'cancel_order')) as temp
where counter > 1
limit(10);
