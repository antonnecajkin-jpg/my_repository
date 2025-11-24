from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# === СИСТЕМНЫЕ СТРОКИ ===
def my_custom_function():
    """ВАША ЛОГИКА ЗДЕСЬ"""
    # === ПОЛЬЗОВАТЕЛЬСКИЕ СТРОКИ ===
    
    # 1. Создаем хук
    hook = PostgresHook(postgres_conn_id='my_greenplum')
    
    # 2. Выполняем сложную логику
    # Например: несколько запросов + обработка результатов
    
    # Получаем данные
    records = hook.get_records("SELECT * FROM users WHERE active = true")
    
    # Обрабатываем их
    for record in records:
        user_id, name = record
        # Какая-то бизнес-логика...
        print(f"Обрабатываем пользователя: {name}")
        
    # Сохраняем результаты
    hook.run("UPDATE users SET processed = true WHERE active = true")

default_args = {
    'owner': 'your_name',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'my_hook_dag',                              # Имя DAG
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',                 # Расписание
    catchup=False,
    tags=['greenplum']
) as dag:
    
    # === СИСТЕМНЫЕ СТРОКИ ===
    custom_task = PythonOperator(
        task_id='custom_task',
        python_callable=my_custom_function      # Ваша функция
    )