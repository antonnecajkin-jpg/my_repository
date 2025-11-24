from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def test_greenplum_connection():
    hook = PostgresHook(postgres_conn_id="my_greenplum")
    
    # Проверяем версию Greenplum
    version = hook.get_first("SELECT version();")
    print("=== Greenplum Version ===")
    print(version[0])
    
    # Создаем тестовую таблицу
    hook.run("""
        CREATE TABLE IF NOT EXISTS airflow_greenplum_test (
            id INT,
            name TEXT,
            created_at TIMESTAMP
        ) DISTRIBUTED BY (id);
    """)
    
    # Вставляем тестовые данные
    hook.run("""
        INSERT INTO airflow_greenplum_test VALUES 
        (1, 'Test User 1', NOW()),
        (2, 'Test User 2', NOW());
    """)
    
    # Читаем данные
    results = hook.get_records("SELECT * FROM airflow_greenplum_test")
    print("=== Test Data ===")
    for row in results:
        print(row)

with DAG('test_greenplum_workflow',
         start_date=datetime(2023, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:

    test_greenplum = PythonOperator(
        task_id='test_greenplum_database',
        python_callable=test_greenplum_connection
    )