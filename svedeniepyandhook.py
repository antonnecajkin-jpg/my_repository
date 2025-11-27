def complex_etl():
    hook = PostgresHook(postgres_conn_id='my_greenplum')
    
    # EXTRACT - читаем данные из исходной таблицы orders
    raw_data = hook.get_records("""
        SELECT user_id, order_date, amount 
        FROM orders 
        WHERE order_date >= '2024-01-01'
    """)
    
    # TRANSFORM - обрабатываем и добавляем категорию
    processed_data = []
    for user_id, order_date, amount in raw_data:
        # Добавляем бизнес-логику (категоризацию)
        if amount > 1000:
            category = "VIP"
        elif amount > 500:
            category = "Standard" 
        else:
            category = "Economy"
            
        processed_data.append((user_id, order_date, amount, category))
    
    # LOAD - записываем в ЦЕЛЕВУЮ таблицу order_stats (с категорией)
    for user_id, order_date, amount, category in processed_data:
        hook.run(f"""
            INSERT INTO order_stats (user_id, order_date, amount, category)
            VALUES ({user_id}, '{order_date}', {amount}, '{category}')
        """)