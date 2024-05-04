# We'll start by importing the DAG object
from datetime import timedelta, datetime
from pathlib import Path

from airflow import DAG
# We need to import the operators used in our tasks

from airflow.operators.python import PythonOperator

# We then import the days_ago function
from airflow.utils.dates import days_ago

import pandas as pd
import sqlite3
import os,sys

import sys
from pathlib import Path

# Add the project root directory to the Python path


# get dag directory path
dag_path = os.getcwd()

sys.path.append('dags/scripts')

import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Import ELT using the absolute path
from scripts.load import ELT



#from scripts.load import ELT

##########################################################################
# In elt_dag.py
import os

dag_path = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(dag_path, 'data')
file_path = os.path.join(data_dir, '20181024_d3_1030_1100.csv')

elt = ELT('./data/20181024_d3_1030_1100.csv',
         './data/extracted_file/')
#########################################################################


# initializing the default arguments that we'll pass to our DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(5)
}

ingestion_dag = DAG(
     'data_traffic_ingestion',
    default_args=default_args,
    description='Aggregates booking records for data analysis',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    user_defined_macros={'date_to_millis': elt.execution_date_to_millis}
   
)
ingestion_dag.schedule = '@once'

task_1 = PythonOperator(
    task_id='extract_data',
    python_callable=elt.extract_data,
    # op_args=["{{ ds }} {{ execution_date.hour }}"],
    dag=ingestion_dag,
    
)

task_2 = PythonOperator(
    task_id='load_vehicle_data',
    python_callable=elt.load_vehicle_data,
    # op_args=["{{ ds }} {{ execution_date.hour }}"],
    dag=ingestion_dag,
)

task_3 = PythonOperator(
    task_id='load_trajectory_data',
    python_callable=elt.load_trajectory_data,
    # op_args=["{{ ds }} {{ execution_date.hour }}"],
    dag=ingestion_dag,
)

task_1 >> task_2 
task_1 >> task_3