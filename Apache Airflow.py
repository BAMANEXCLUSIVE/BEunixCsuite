pip install apache-airflow

import os
import subprocess

def generate_gantt_chart():
    gantt_code = """
    @startgantt
    Project starts 2025-03-01

    [Initiation] lasts 30 days
    [Initiation] is 50% completed
    [Initiation] links to https://github.com/BAMANEXCLUSIVE/BEunixCsuite/blob/main/docs/Initiation.md

    [Planning] lasts 60 days
    [Planning] is 20% completed
    [Planning] links to https://github.com/BAMANEXCLUSIVE/BEunixCsuite/blob/main/docs/Planning.md

    [Execution] lasts 60 days
    [Execution] is 10% completed
    [Execution] links to https://github.com/BAMANEXCLUSIVE/BEunixCsuite/blob/main/docs/Execution.md

    [Monitoring and Controlling] lasts 30 days
    [Monitoring and Controlling] is 0% completed
    [Monitoring and Controlling] links to https://github.com/BAMANEXCLUSIVE/BEunixCsuite/blob/main/docs/Monitoring_and_Controlling.md

    [Closing] lasts 30 days
    [Closing] is 0% completed
    [Closing] links to https://github.com/BAMANEXCLUSIVE/BEunixCsuite/blob/main/docs/Closing.md

    @endgantt
    """
    
    with open("gantt_chart.puml", 'w') as file:
        file.write(gantt_code)

def generate_airflow_dag():
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
    
    with open("gantt_chart_dag.py", 'w') as file:
        file.write(dag_code)

def configure_auto_start():
    service_file_content = """
    [Unit]
    Description=Apache Airflow scheduler
    After=network.target

    [Service]
    User=airflow
    Group=airflow
    Environment="AIRFLOW_HOME=/path/to/airflow"
    ExecStart=/path/to/airflow/bin/airflow scheduler
    Restart=always
    RestartSec=5s

    [Install]
    WantedBy=multi-user.target
    """
    
    with open("/etc/systemd/system/airflow-scheduler.service", 'w') as file:
        file.write(service_file_content)
    
    subprocess.run(["sudo", "systemctl", "enable", "airflow-scheduler"])
    subprocess.run(["sudo", "systemctl", "start", "airflow-scheduler"])

def main():
    generate_gantt_chart()
    generate_airflow_dag()
    configure_auto_start()
    subprocess.run(["airflow", "dags", "trigger", "gantt_chart_dag"])

if __name__ == "__main__":
    main()
