from pyspark.sql.functions import broadcast

# Example of using broadcast join
joined_df = large_df.join(broadcast(small_df), "key")