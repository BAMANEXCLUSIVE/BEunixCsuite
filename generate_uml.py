import os

def generate_uml(output_file):
    uml_code = """
    @startuml
    ' Define parent class
    class ParentClass {
        + String parentAttribute
        + void parentMethod()
    }
    
    ' Define child class
    class ChildClass {
        + String childAttribute
        + void childMethod()
    }
    
    ' Relationship
    ParentClass <|-- ChildClass

    ' Add hyperlinks
    ParentClass : [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]]
    ChildClass : [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]]

    note right of ParentClass
      This is the ParentClass. For more details, visit
      [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]].
    end note

    note right of ChildClass
      This is the ChildClass. For more details, visit
      [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]].
    end note
    @enduml
    """
    
    with open(output_file, 'w') as file:
        file.write(uml_code)

def generate_gantt_chart(output_file):
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
    
    with open(output_file, 'w') as file:
        file.write(gantt_code)

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
    uml_output_file = "diagram.puml"
    gantt_output_file = "gantt_chart.puml"
    dag_output_file = "gantt_chart_dag.py"
    
    generate_uml(uml_output_file)
    generate_gantt_chart(gantt_output_file)
    generate_airflow_dag(dag_output_file)
    
    print(f"PlantUML code written to {uml_output_file}")
    print(f"Gantt chart code written to {gantt_output_file}")
    print(f"Airflow DAG code written to {dag_output_file}")
