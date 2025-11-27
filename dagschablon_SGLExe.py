# === СИСТЕМНЫЕ ИМПОРТЫ ===
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

# === СИСТЕМНЫЕ НАСТРОЙКИ ===
default_args = {
    'owner': 'your_name',                    # ⚙️ Ваше имя для мониторинга
    'retries': 1,                           # ⚙️ Количество повторных попыток
    'retry_delay': timedelta(minutes=5)     # ⚙️ Задержка между попытками
}

# === СИСТЕМНОЕ СОЗДАНИЕ DAG ===
with DAG(
    'my_sql_query_dag',                     # 📝 Ваше имя DAG
    default_args=default_args,              # ⚙️ Применяем настройки выше
    start_date=datetime(2024, 1, 1),        # ⚙️ Дата начала выполнения
    schedule_interval='@daily',             # ⚙️ Расписание (@daily, @hourly и т.д.)
    catchup=False,                          # ⚙️ Не выполнять пропущенные запуски
    tags=['etl', 'sql']                     # 🏷️ Ваши теги для фильтрации
) as dag:

    # === ПОЛЬЗОВАТЕЛЬСКАЯ ЗАДАЧА ===
    sql_task = SQLExecuteQueryOperator(
        # === СИСТЕМНЫЕ ПАРАМЕТРЫ ===
        task_id='execute_complex_sql',      # 📝 Ваш уникальный ID задачи
        conn_id='my_greenplum',             # 🔗 Ваш connection из Airflow
        
        # === ПОЛЬЗОВАТЕЛЬСКИЙ SQL ===
        sql=[
            # 📋 Запрос 1: Создание таблицы (ЕСЛИ НУЖНО)
            """
            CREATE TABLE IF NOT EXISTS my_report_table (
                id SERIAL PRIMARY KEY,
                report_date DATE,
                total_users INTEGER,
                total_orders INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # 📋 Запрос 2: Очистка старых данных (ЕСЛИ НУЖНО)  
            """
            DELETE FROM my_report_table 
            WHERE report_date = CURRENT_DATE;
            """,
            
            # 📋 Запрос 3: Основная бизнес-логика - ВАША!
            """
            INSERT INTO my_report_table (report_date, total_users, total_orders)
            SELECT 
                CURRENT_DATE as report_date,
                COUNT(DISTINCT user_id) as total_users,
                COUNT(*) as total_orders
            FROM orders 
            WHERE order_date = CURRENT_DATE - INTERVAL '1 day';
            """,
            
            # 📋 Запрос 4: Проверка результатов - ВАША!
            """
            SELECT report_date, total_users, total_orders 
            FROM my_report_table 
            WHERE report_date = CURRENT_DATE;
            """
        ],
        
        # === ПОЛЬЗОВАТЕЛЬСКАЯ ОБРАБОТКА РЕЗУЛЬТАТОВ (ОПЦИОНАЛЬНО) ===
        handler=lambda results: 
            print(f"✅ Создана таблица, вставлены данные. Результат: {results[3]}"),
        
        # === СИСТЕМНЫЕ ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ ===
        autocommit=True,                    # ⚙️ Автоматическое подтверждение
        show_return_value_in_logs=True      # ⚙️ Показывать результаты в логах
    )

# === СИСТЕМНОЕ: НЕТ ДОПОЛНИТЕЛЬНЫХ ЗАВИСИМОСТЕЙ ===
# Задача выполняется независимо