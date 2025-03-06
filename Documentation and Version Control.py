import os
import json
from datetime import datetime

def generate_documentation(version):
    doc_content = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "description": "ETL Pipeline Documentation",
        "functions": [
            {"name": "extract", "description": "Extracts data from source."},
            {"name": "transform", "description": "Transforms the extracted data."},
            {"name": "load", "description": "Loads data into target database."}
        ]
    }
    
    with open(f'documentation/version_{version}.json', 'w') as f:
        json.dump(doc_content, f)

def check_and_create_version():
    version = len(os.listdir('documentation')) + 1  # Increment version based on existing files
    os.makedirs('documentation', exist_ok=True)
    
    generate_documentation(version)
    
check_and_create_version()