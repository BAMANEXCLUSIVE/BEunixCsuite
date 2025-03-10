from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

def extract():
    # Extract data from a CSV file
    df = pd.read_csv('data/source_data.csv')
    return df

def transform(df):
    # Transform the data: e.g., cleaning or aggregating
    df.dropna(inplace=True)  # Remove missing values
    df['total'] = df['quantity'] * df['price']  # Example transformation
    return df

def load(df):
    # Load data into PostgreSQL database
    engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
    df.to_sql('target_table', engine, if_exists='replace', index=False)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

with DAG('etl_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    extract_task = PythonOperator(task_id='extract', python_callable=extract)
    transform_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)

    extract_task >> transform_task >> load_task  # Set task dependencies