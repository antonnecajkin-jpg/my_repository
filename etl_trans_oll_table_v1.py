from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def etl_trans_from_raw_to_core():
    hook_gp = PostgresHook(postgres_conn_id='my_greenplum')

    table_mappings = {
        'raw.users': {
            'core.dim_user': [
                'user_id',
                'name', 
                'age',
                'email',
                'registration_date'
            ]
        },
        'raw.courses': {
            'core.dim_course': [
                'course_id',
                'title',
                'category'
            ]
        },
        'raw.lessons': {
            'core.dim_lesson': [
                'lesson_id',
                'title',
                'duration_min',
                'course_id'
            ]
        }
    }
    
    for source_table, target_mapping in table_mappings.items():
        for target_table, columns in target_mapping.items():
            count_sql = f"SELECT COUNT(*) FROM {target_table}"
            target_count = hook_gp.get_first(count_sql)
            
            columns_str = ", ".join(columns)
            primary_key = columns[0] 
            
            if target_count[0] == 0:
                hook_gp.run(f"""
                INSERT INTO {target_table} ({columns_str})
                SELECT {columns_str}
                FROM {source_table}
            """)
            else:
                hook_gp.run(f"""
                INSERT INTO {target_table} ({columns_str})
                SELECT {columns_str}
                FROM {source_table} s
                LEFT JOIN {target_table} t ON s.{primary_key} = t.{primary_key}
                WHERE t.{primary_key} IS NULL
            """)
            
            


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_raw_to_core',
    default_args=default_args,
    description='ETL from raw to core layer',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    etl_task = PythonOperator(
        task_id='transform_raw_to_core',
        python_callable=etl_trans_from_raw_to_core
    )

    