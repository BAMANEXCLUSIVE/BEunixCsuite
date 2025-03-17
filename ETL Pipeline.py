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

def generate_airflow_dag(dag_file):
    dag_code = """
    from airflow import DAG
    from airflow.operators.dummy_operator import DummyOperator
    from datetime import datetime

    default_args = {
        'owner': 'airflow',
        'start_date': datetime(2025, 3, 1),
    }

    dag = DAG('gantt_chart_dag', default_args=default_args, schedule_interval='@daily')

    start = DummyOperator(task_id='start', dag=dag)
    initiation = DummyOperator(task_id='initiation', dag=dag)
    planning = DummyOperator(task_id='planning', dag=dag)
    execution = DummyOperator(task_id='execution', dag=dag)
    monitoring = DummyOperator(task_id='monitoring', dag=dag)
    closing = DummyOperator(task_id='closing', dag=dag)

    start >> initiation >> planning >> execution >> monitoring >> closing
    """
    
    with open(dag_file, 'w') as file:
        file.write(dag_code)

if __name__ == "__main__":
    dag_output_file = "gantt_chart_dag.py"
    generate_airflow_dag(dag_output_file)
    print(f"Airflow DAG code written to {dag_output_file}")
