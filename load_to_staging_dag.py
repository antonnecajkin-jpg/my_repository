from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Anti',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'create_schemas',                          
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,                 
    catchup=False
) as dag:
    
    sql_task = SQLExecuteQueryOperator(
        task_id='create_raw_core_dm',      
        conn_id='my_greenplum',

        sql = [ 
                """
                CREATE SCHEMA raw;  
                """,    
                """
                CREATE SCHEMA core;  
                """,     
                """
                CREATE SCHEMA dm;  
                """


        ]
    )
    