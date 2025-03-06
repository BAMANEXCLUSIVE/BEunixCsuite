import os
import subprocess

def initialize_project():
    # Create a virtual environment
    subprocess.call(['python', '-m', 'venv', 'env'])
    # Activate the virtual environment (Windows)
    os.system('env\\Scripts\\activate')
    # Install required packages
    packages = ['numpy', 'pandas', 'scikit-learn', 'matplotlib']
    subprocess.call(['pip', 'install'] + packages)

initialize_project()