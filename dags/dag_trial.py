from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def load_csv_to_airflow(file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Perform any necessary data processing or transformations here
        
        # You can now use the DataFrame 'df' in your Airflow tasks
        print(df.head())
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        raise

with DAG('try_dag', default_args=default_args, schedule_interval=None) as dag:
    load_task = PythonOperator(
        task_id='load_csv_to_airflow',
        python_callable=load_csv_to_airflow,
        op_kwargs={
            'file_path': os.path.join(os.path.dirname(__file__), 'data', '20181024_d3_1030_1100.csv')
        }
    )

