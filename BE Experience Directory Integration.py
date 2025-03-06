import os

def create_directories(base_path, subdirs):
    """Create directories if they do not exist."""
    for subdir in subdirs:
        path = os.path.join(base_path, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'Created directory: {path}')
        else:
            print(f'Directory already exists: {path}')

def list_directories(base_path):
    """List all subdirectories in the given base path."""
    print(f'Contents of {base_path}:')
    for root, dirs, files in os.walk(base_path):
        print(f'\nCurrent Directory: {root}')
        for dir in dirs:
            print(f'- {dir}')

# Define existing paths
be_experience_workplace_path = r'C:\Users\user\Documents\BE_Experience_Workplace'
system_in_administrator_path = r'C:\Users\user\Documents\System_in_Administrator'

# Define required subdirectories for BE Experience Workplace
be_subdirectories = [
    'Logic_Functions',
    'Integration_Scripts',
    'Backup_Scripts',
]

# Define required subdirectories for System in Administrator
system_subdirectories = [
    'Original_Software',
    'Libraries',
    'Essentials',
]

# Create BE Experience Workplace and its subdirectories
create_directories(be_experience_workplace_path, be_subdirectories)

# Create System in Administrator and its subdirectories
create_directories(system_in_administrator_path, system_subdirectories)

# List the final structure of the directories created
list_directories(be_experience_workplace_path)
list_directories(system_in_administrator_path)