from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def from_psql_in_pg():
    hook_psql = PostgresHook(postgres_conn_id='my_postgres_db')
    hook_gp = PostgresHook(postgres_conn_id='my_greenplum')
    
    tables = ['users', 'courses', 'lessons', 'enrollments', 'lesson_views']

    for table in tables:
        records_psql = hook_psql.get_records(f"SELECT * FROM {table}")
        records_gp = hook_gp.get_records(f"SELECT * FROM raw.{table}")
    
        if records_gp == []:
            for record in records_psql:
                hook_gp.run(
                    f"INSERT INTO raw.{table} VALUES ({', '.join(['%s'] * len(record))})",
                    parameters=record
                )
        else:   
            max_id_gp = max(record[0] for record in records_gp) 
            for record in records_psql:
                if record[0] > max_id_gp: 
                    hook_gp.run(
                        f"INSERT INTO raw.{table} VALUES ({', '.join(['%s'] * len(record))})",
                        parameters=record
                    )


default_args = {
    'owner': 'your_name',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'my_hook_dag',                             
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,                 
    catchup=False
) as dag:
    
    extract = PythonOperator(
        task_id='extract_for_gp',
        python_callable=from_psql_in_pg      
    )