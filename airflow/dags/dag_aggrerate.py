import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Параметры по умолчанию
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 9, 18),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Определяем DAG
dag = DAG(
    "aggregate_weekly_data",
    default_args=default_args,
    description="DAG для агрегации данных",
    schedule_interval="0 7 * * *",  # Каждый день в 7:00
)


# Функция для выполнения агрегации
def run_aggregation_script():
    os.system(
        "python3 /opt/airflow/dags/script-output.py /opt/airflow/input /opt/airflow/temp /opt/airflow/output 2024-09-18"
    )


# Оператор для запуска Python скрипта
run_script = PythonOperator(
    task_id="run_aggregation_script",
    python_callable=run_aggregation_script,
    dag=dag,
)
