#!/bin/bash

# Set Environment Variables
export DB_USER="postgres"
export DB_PASS="NewSecurePassword123!"
export DB_NAME="airflow_db"
export GCLOUD_USER="azman.jadi@gmail.com"
export GCLOUD_PASS="NoorAzman830726!"
export GITHUB_USER="BAMANEXCLUSIVE"
export GITHUB_TOKEN="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"
export AIRFLOW_USER="BEadmin"
export AIRFLOW_PASS="NoorAzman830726!"

# Function to Edit pg_hba.conf
edit_pg_hba_conf() {
  sudo tee /etc/postgresql/16/main/pg_hba.conf <<EOF
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
local   replication     all                                     md5
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
host    all             BEAdmin          127.0.0.1/32            md5
host    all             postgres         127.0.0.1/32            md5
EOF
}

# Function to Restart PostgreSQL Service
restart_postgresql() {
  sudo systemctl restart postgresql@16-main
}

# Function to Reset Passwords for Users
reset_user_passwords() {
  PGPASSWORD=$DB_PASS psql -U postgres <<EOF
ALTER USER BEAdmin WITH LOGIN PASSWORD 'NoorAzman830726!';
ALTER USER postgres WITH LOGIN PASSWORD 'NewSecurePassword123!';
EOF
}

# Function to Grant Privileges to BEAdmin
grant_privileges() {
  PGPASSWORD=$DB_PASS psql -U postgres <<EOF
GRANT CONNECT ON DATABASE airflow_db TO BEAdmin;
GRANT USAGE ON SCHEMA public TO BEAdmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO BEAdmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO BEAdmin;
EOF
}

# Function to Clear Password Cache
clear_password_cache() {
  rm -f ~/.pgpass
}

# Function to Automate Task Execution
automate_tasks() {
  # PostgreSQL
  PGPASSWORD=$DB_PASS psql -d $DB_NAME -U $DB_USER <<EOF
  \l
  \du
EOF

  # Google Cloud SDK
  gcloud auth login $GCLOUD_USER --quiet

  # GitHub
  export GITHUB_TOKEN=$GITHUB_TOKEN

  # Airflow
  PGPASSWORD=$AIRFLOW_PASS airflow users create --username $AIRFLOW_USER --firstname Firstname --lastname Lastname --role Admin --email $AIRFLOW_USER@example.com
}

# Function to Apply Diff Codespace
apply_diff_codespace() {
  echo "Applying diff codespace..."
  # Add your diff codespace logic here
}

# Function to Download Diffs Codespace
download_diffs_codespace() {
  echo "Downloading diffs codespace..."
  # Add your download diffs codespace logic here
}

# Main Function
main() {
  edit_pg_hba_conf
  restart_postgresql
  reset_user_passwords
  clear_password_cache
  grant_privileges
  automate_tasks

  # Apply and download diffs codespace
  apply_diff_codespace
  download_diffs_codespace

  # Loop to continue tasks
  while true; do
    echo "Re-running the script to complete the tasks..."
    ./automate_tasks.sh
    sleep 10  # Add a delay to avoid rapid looping
  done
}

# Run the Main Function
main
