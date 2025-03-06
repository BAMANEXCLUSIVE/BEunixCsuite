# Example of writing partitioned data
updated_data_df.write.partitionBy("date").format("delta").mode("overwrite").save("path/to/updated_table")