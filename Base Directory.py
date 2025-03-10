import os

# Base directory
base_dir = 'C:\\Users\\user\\Documents'

# Create directories
be_experience_workplace = os.path.join(base_dir, 'BE_Experience_Workplace')
logic_functions = os.path.join(be_experience_workplace, 'Logic_Functions')
integration_scripts = os.path.join(be_experience_workplace, 'Integration_Scripts')
backup_scripts = os.path.join(be_experience_workplace, 'Backup_Scripts')
system_in_administrator = os.path.join(base_dir, 'System_in_Administrator')
original_software = os.path.join(system_in_administrator, 'Original_Software')
libraries = os.path.join(system_in_administrator, 'Libraries')
essentials = os.path.join(system_in_administrator, 'Essentials')

# Make directories
for directory in [be_experience_workplace, logic_functions, integration_scripts, backup_scripts, system_in_administrator, original_software, libraries, essentials]:
    os.makedirs(directory, exist_ok=True)

print(f"BE Experience Workplace: {be_experience_workplace}")
print(f"System in Administrator: {system_in_administrator}")
