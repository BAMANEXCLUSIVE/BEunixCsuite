# Example of watermarking
max_timestamp = existing_data_df.selectExpr("max(timestamp)").collect()[0][0]
new_records_df = new_data_df.filter(new_data_df.timestamp > max_timestamp)