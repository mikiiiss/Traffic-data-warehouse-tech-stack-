from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator



from datetime import datetime
from random import randint
import math

def best_performing_model(ti):
    result = ti.xcom_pull(task_ids=[
        'model_1',
        'model_2'
    ])
    if max(result) > 20:
       return "True"
    return "False"

def model (model):
    random_num = randint(2, 10)
    result = math.sqrt(random_num)
    return result

with DAG("cry_dag",
    start_date=datetime(2024, 5,1),
    schedule_interval='@daily',
    tags=["DE"],
    catchup=False) as dag:

    training_model_tasks = [
        PythonOperator(
            task_id=f"model_{model_id}",
            python_callable=model,
            op_kwargs={
                "model": model_id
            }
        ) for model_id in ['1', '2']

    ]

    best_performing_model = BranchPythonOperator(
        task_id="best_performing_model",
        python_callable=best_performing_model
    )

    Success = BashOperator(
        task_id="True",
        bash_command=" echo 'Success'"
    )
    Failed = BashOperator(
        task_id="False",
        bash_command=" echo 'Failed'"
    )
    training_model_tasks >> best_performing_model >> [Success, Failed]


