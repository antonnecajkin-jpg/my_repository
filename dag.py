from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def push_data_1(ti):
    ti.xcom_push(key='num_1', value=1)

def push_data_2(ti):
    ti.xcom_push(key='num_2', value=2)

def push_data_3(ti):
    ti.xcom_push(key='num_3', value=3)
 
def pull_data(ti):
    # Получаем все три значения по их ключам
    num_1 = ti.xcom_pull(key='num_1', task_ids='push_1')
    num_2 = ti.xcom_pull(key='num_2', task_ids='push_2')
    num_3 = ti.xcom_pull(key='num_3', task_ids='push_3')
    
    # Суммируем значения
    total_sum = num_1 + num_2 + num_3
    print(f"Сумма всех значений: {total_sum}")
    
    # Можно также вернуть результат
    return total_sum

dag = DAG(
    dag_id="multi_task_xcom_pull", 
    start_date=datetime(2025,1,1), 
    schedule_interval=None,
    catchup=False
)

# Таски для отправки данных
push_1 = PythonOperator(
    task_id='push_1',
    python_callable=push_data_1,
    dag=dag
)

push_2 = PythonOperator(
    task_id='push_2',
    python_callable=push_data_2,
    dag=dag
)

push_3 = PythonOperator(
    task_id='push_3',
    python_callable=push_data_3,
    dag=dag
)

# Таска для получения и суммирования данных
sum_all = PythonOperator(
    task_id='sum_all',
    python_callable=pull_data,
    dag=dag
)

# Определяем порядок выполнения
push_1 >> push_2 >> push_3 >> sum_all