from sqlalchemy import create_engine, text

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

# Function to perform atomic MERGE operation
def merge_data(engine):
    with engine.connect() as connection:
        # Start a transaction
        with connection.begin():
            # Define the MERGE SQL statement
            merge_sql = """
            INSERT INTO target_table (id, name, value)
            SELECT id, name, value FROM source_table
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name,
                value = EXCLUDED.value;
            """

            # Execute the MERGE operation
            connection.execute(text(merge_sql))
            print("Merge operation completed successfully.")

def main():
    # Create database connection
    engine = create_db_connection()

    # Perform the MERGE operation
    merge_data(engine)

if __name__ == "__main__":
    main()