# Import necessary libraries and modules
import sys
from typing_extensions import Self

from data_reader import DataReader
from db_connection import create_tables, insert_data

from datetime import datetime, timedelta
import pandas as pd
import os
# Get the current working directory
dag_path = os.getcwd()
print(dag_path)
# Class definition for Extract, Load, Transform (ELT)
# TRAJECTORY_SCHEMA = os.path.join(
#     dag_path, "scripts/trajectory_schema.sql")
# VEHICLE_SCHEMA = os.path.join(dag_path, "scripts/vehicle_schema.sql")

TRAJECTORY_SCHEMA = os.path.join(dag_path, "scripts/trajectory_schema.sql")
VEHICLE_SCHEMA = os.path.join(dag_path, "scripts/vehicle_schema.sql")
# TRAJECTORY_SCHEMA = "trajectory_schema.sql"
# VEHICLE_SCHEMA = "vehicle_schema.sql"

# # Now, you can use these filenames with the current working directory
# trajectory_schema_path = os.path.join(dag_path, TRAJECTORY_SCHEMA)
# vehicle_schema_path = os.path.join(dag_path, VEHICLE_SCHEMA)


class ELT:
    def __init__(self, read_dag_path,save_dag_path):
        self.read_dag_path = read_dag_path
        self.save_dag_path = save_dag_path

    def extract_data(self,file_path=None,) -> None:
         # Allow overriding the default file path if provided
        if file_path is not None:
            self.read_dag_path = file_path
        
        # Use DataReader to get DataFrames from the specified file path
        reader = DataReader()
        vehicle_df, trajectories_df = reader.get_dfs(
            file_path=self.read_dag_path, v=0)
        print(file_path)
        
        vehicle_df.to_csv(os.path.join(self.save_dag_path,'vehicle_info.csv'),index=False)
        trajectories_df.to_csv(os.path.join(self.save_dag_path,'trajectories_info.csv'), index=False)
        # print(vehicle_df.head())
        
         # Instead of saving to specified paths, save to local directory for now
        # vehicle_df.to_csv('vehicle_info.csv', index=False)
        # trajectories_df.to_csv('trajectories_info.csv', index=False)
        
        
        # Load trajectories data from CSV file and insert into the database
    def load_trajectory_data(self):
        trajectories_df = pd.read_csv(os.path.join(self.save_dag_path, 'trajectories_info.csv'))
        create_tables(TRAJECTORY_SCHEMA)
        print('create trajectory table')
        insert_data(trajectories_df[:10000], "trajectories")
    
     # Load vehicle data from CSV file and insert into the database
    def load_vehicle_data(self):
        vehicle_df = pd.read_csv(os.path.join(
            self.save_dag_path, 'vehicle_info.csv'))
        create_tables(VEHICLE_SCHEMA)
        print('create vehicle table')
        insert_data(vehicle_df, "vehicles")
        
    def execution_date_to_millis(self, execution_date):
        
        """converts execution date (in DAG timezone) to epoch millis

        Args:
            date (execution date): %Y-%m-%d

        Returns:
            milliseconds
        """
        date = datetime.strptime(execution_date, "%Y-%m-%d")
        epoch = datetime.utcfromtimestamp(0)
        return (date - epoch).total_seconds() * 1000.0






# elt = ELT('./data/20181029_d1_0900_0930.csv',
#          './data/extracted_file')




# # # elt.extract_data()

# # elt.load_vehicle_data()
# elt.load_trajectory_data()