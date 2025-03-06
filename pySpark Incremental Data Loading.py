from pyspark.sql import SparkSession
from pyspark.sql.functions import max

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Incremental Data Load Example") \
    .getOrCreate()

# Load existing data
existing_data_df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .load("path/to/existing_data.csv")

# Load new data
new_data_df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .load("path/to/new_data.csv")

# Identify the latest timestamp in existing data
max_timestamp = existing_data_df.select(max("timestamp")).collect()[0][0]

# Filter new records based on the latest timestamp
new_records_df = new_data_df.filter(new_data_df.timestamp > max_timestamp)

# Check if there are new records to append
if not new_records_df.isEmpty():
    # Append new records to existing data
    updated_data_df = existing_data_df.union(new_records_df)
    
    # Write updated data back to storage (overwrite or append)
    updated_data_df.write \
        .format("csv") \
        .mode("overwrite") \
        .option("header", "true") \
        .save("path/to/updated_data.csv")
    
    print(f"Appended {new_records_df.count()} new records.")
else:
    print("No new records to append.")

# Stop Spark session
spark.stop()