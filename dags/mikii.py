from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
import pandas as pd

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo", start_date=datetime.today(), schedule="0 0 * * *") as dag:
    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    @task()
    def read_csv():
        # Read the CSV file
        df = pd.read_csv('/opt/airflow/data/20181024_d1_0830_0900.csv')

        # Perform some basic checks on the data
        print(f"Number of rows: {len(df)}")
        print(f"Column names: {df.columns}")
        print(f"First 5 rows:\n{df.head()}")

        return df

    # Set dependencies between tasks
    hello >> airflow() >> read_csv()
