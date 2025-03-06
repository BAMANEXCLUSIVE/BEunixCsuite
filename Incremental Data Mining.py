import pandas as pd
from sqlalchemy import create_engine
import os

# Database configuration
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'your_database'

# Create a connection to the database
def create_db_connection():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    return engine

# Function to get the last processed ID from a checkpoint file
def get_last_processed_id(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return int(f.read().strip())
    return 0  # Default to 0 if no checkpoint exists

# Function to update the checkpoint file with the latest processed ID
def update_checkpoint(checkpoint_file, last_id):
    with open(checkpoint_file, 'w') as f:
        f.write(str(last_id))

# Function to extract incremental data from the database
def extract_incremental_data(engine, last_processed_id):
    query = f"""
    SELECT * FROM your_table
    WHERE id > {last_processed_id}
    ORDER BY id ASC;
    """
    return pd.read_sql(query, engine)

# Function to process the extracted data (transform)
def process_data(df):
    # Example transformation: clean and prepare data
    df.dropna(inplace=True)  # Remove missing values
    # Add more processing logic as needed
    return df

# Function to load processed data into another table or system
def load_data(df, engine):
    df.to_sql('processed_table', engine, if_exists='append', index=False)

def main():
    checkpoint_file = 'checkpoint.txt'
    
    # Create database connection
    engine = create_db_connection()

    # Get last processed ID from checkpoint file
    last_processed_id = get_last_processed_id(checkpoint_file)

    # Extract new incremental data
    new_data = extract_incremental_data(engine, last_processed_id)

    if not new_data.empty:
        # Process the new data
        processed_data = process_data(new_data)

        # Load processed data into the target table or system
        load_data(processed_data, engine)

        # Update checkpoint with the latest processed ID
        last_id = new_data['id'].max()  # Assuming 'id' is the primary key
        update_checkpoint(checkpoint_file, last_id)
        print(f"Processed and loaded {len(processed_data)} new records.")
    else:
        print("No new records to process.")

if __name__ == "__main__":
    main()