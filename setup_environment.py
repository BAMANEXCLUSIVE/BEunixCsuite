import subprocess
import os

def setup_environment():
    # Create a virtual environment
    subprocess.call(['python', '-m', 'venv', 'env'])
    
    # Activate the virtual environment (Windows)
    os.system('env\\Scripts\\activate')
    
    # Install required packages for ETL processing
    packages = ['apache-airflow', 'pandas', 'sqlalchemy']
    subprocess.call(['pip', 'install'] + packages)

setup_environment()

import os

def setup_environment():
    print("Setting up environment...")

if __name__ == "__main__":
    setup_environment()
    print("Environment setup complete.")

