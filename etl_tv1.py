from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def etl_trans_from_raw_to_core():
    hook_gp = PostgresHook(postgres_conn_id='my_greenplum')
    
    dim_user_count = hook_gp.get_first("SELECT COUNT(*) FROM core.dim_user")
    
    if dim_user_count[0] == 0:
        hook_gp.run("""
            INSERT INTO core.dim_user (user_id, name, age, email, registration_date)
            SELECT DISTINCT
                user_id::INT,
                name::TEXT,
                age::INT,
                email::TEXT, 
                registration_date::DATE
            FROM raw.users
            WHERE user_id IS NOT NULL;
        """)
    else:
        hook_gp.run("""
            INSERT INTO core.dim_user (user_id, name, age, email, registration_date)
            SELECT DISTINCT
                r.id::INT,
                r.name::TEXT, 
                r.age::INT,
                r.email::TEXT,
                r.registration_date::DATE
            FROM raw.users r
            LEFT JOIN core.dim_user c ON r.id = c.user_id
            WHERE c.user_id IS NULL
            AND r.id IS NOT NULL;
        """)

default_args = {
    'owner': 'Anti',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'insert_dim_user_v2',                             
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,                 
    catchup=False
) as dag:
    
    extract = PythonOperator(
        task_id='first_dim_to_core_v2',
        python_callable=etl_trans_from_raw_to_core      
    )