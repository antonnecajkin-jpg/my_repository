from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# === СИСТЕМНЫЕ СТРОКИ ===
default_args = {
    'owner': 'Anti',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'my_operator_dag',                          # Имя DAG
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',                 # Расписание
    catchup=False,
    tags=['greenplum']
) as dag:
    
    # === ПОЛЬЗОВАТЕЛЬСКИЕ СТРОКИ ===
    # Просто добавляете задачи с SQL запросами
    
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='my_greenplum',        # Connection из Airflow
        sql='''
            CREATE TABLE IF NOT EXISTS my_table (
                id INT,
                name TEXT
            ) DISTRIBUTED BY (id);
        '''
    )
    
    insert_data = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='my_greenplum',
        sql='''
            INSERT INTO my_table VALUES 
            (1, 'John'),
            (2, 'Jane');
        '''
    )
    
    # === СИСТЕМНЫЕ СТРОКИ ===
    # Определяем порядок выполнения
    create_table >> insert_data