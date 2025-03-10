import os
import shutil
import subprocess
from datetime import datetime

def create_updated_project_structure(base_path, project_name):
    """Set up updated project directory structure."""
    print(f"Updating project directory for {project_name}...\n")
    
    # Define new folder structure
    folders = [
        "backups",
        "logs",
        "docs",
        "src/modules",
        "src/utils",
        "tests",
        "data/raw",
        "data/processed",
        "notebooks",
        "scripts",
        "output"
    ]
    
    # Create project base path
    project_path = os.path.join(base_path, project_name)
    os.makedirs(project_path, exist_ok=True)

    # Create folders
    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)
    print(f"Project structure updated at: {project_path}")

    return project_path

def link_to_github(project_path, github_url):
    """Link the local project directory to a GitHub repository."""
    print("\nLinking to GitHub repository...")
    try:
        # Initialize Git repository if not already initialized
        if not os.path.exists(os.path.join(project_path, ".git")):
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            print("Git repository initialized.")

        # Check if remote is already added
        result = subprocess.run(["git", "remote"], cwd=project_path, stdout=subprocess.PIPE, text=True)
        if "origin" in result.stdout:
            print("Remote 'origin' already exists. Skipping remote linking.")
        else:
            subprocess.run(["git", "remote", "add", "origin", github_url], cwd=project_path, check=True)
            print(f"GitHub repository linked: {github_url}")

    except subprocess.CalledProcessError as e:
        print(f"Error linking to GitHub: {e}")

def create_backup(project_path):
    """Create a timestamped backup of the project directory."""
    backup_folder = os.path.join(project_path, "backups")
    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_folder, f"backup_{timestamp}.zip")
    print(f"Creating backup: {backup_file}")
    shutil.make_archive(backup_file.replace('.zip', ''), 'zip', project_path)
    print("Backup created successfully!")

def create_gitignore(project_path):
    """Create a default .gitignore file."""
    gitignore_path = os.path.join(project_path, ".gitignore")
    with open(gitignore_path, "w") as file:
        file.write("\n".join([
            "# Ignore backup and logs folders",
            "backups/",
            "logs/",
            "# Ignore system files",
            ".DS_Store",
            "Thumbs.db",
            "# Ignore editor settings",
            ".vscode/",
        ]))
    print(".gitignore file created.")

# Parameters
base_path = r"C:\Users\user\Documents\BE_Experience_Workplace\BEunixCsuite Workflows"
project_name = "BE Master Project Management"
github_url = "https://github.com/users/BAMANEXCLUSIVE/projects/3"

# Execute updates
project_path = create_updated_project_structure(base_path, project_name)
create_gitignore(project_path)
link_to_github(project_path, github_url)
create_backup(project_path)
