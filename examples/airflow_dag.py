from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2016, 8, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    }

dag = DAG('aws_spot_price_history', default_args=default_args, schedule_interval='@hourly')

run_all = BashOperator(
    task_id='run_all',
    bash_command='aws_spot_price_history --end-time {{ ts }} --action slack --output-dir /tmp/spot-reporter/{{ ts }} r3.8xlarge',
    dag=dag
)
