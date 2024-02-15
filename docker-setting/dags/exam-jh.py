from airflow import DAG
from datetime import datetime
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

# execution date 사용
date = "{{execution_date.strftime('%Y-%m-%d')}}"

# default argument 설정
default_args = {
    'owner': 'jh:1.0.0',
    'depends_on_past': True,
    'start_date': datetime(2022,1,20)
}

# dag 설정
dag = DAG(
    'dag_name_jh',
	default_args=default_args,
	tags=['tag_1','tag_jh'],
	max_active_runs=1,
	schedule_interval="@once")

# start
start = EmptyOperator(
	task_id = 'start',
	dag=dag
)

# curl https://jsonplaceholder.typicode.com/todos/1
curl_demo = BashOperator(
	task_id='curl.demo',
	bash_command=f"""
	curl 'jsonplaceholder.typicode.com/todos/1'
	""",
	dag=dag
)

# finish
finish = EmptyOperator(
	task_id = 'finish',
	dag = dag,
	trigger_rule='all_done'
)

# process
start >> curl_demo >> finish
