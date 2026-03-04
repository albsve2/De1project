from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col
from etl_job import load_and_filter
from config import HDFS_INPUT_PATH, HDFS_OUTPUT_PATH, APP_NAME, MASTER_URL, EXECUTOR_MEMORY, EXECUTOR_CORES, DRIVER_HOST

# Build Spark session
def main():
    spark = (SparkSession.builder #
             .appName(APP_NAME) # Application name
             .master(MASTER_URL) # Where the application is running local or cluster
             .config("spark.executor.memory", EXECUTOR_MEMORY) # Amount of memory per executor
             .config("spark.executor.cores", EXECUTOR_CORES) # Number of cores per executor
             .config("spark.driver.host", DRIVER_HOST) # Master node IP for worker nodes
             .config("spark.driver.bindAddress", DRIVER_HOST) # Master node IP for driver
             .getOrCreate()) # Create Spark session

    df = load_and_filter(spark, HDFS_INPUT_PATH) # Preprocess data

    # Count amount of trips per hour and route
    result = (df.groupBy("pickup_hour", "route")
                .agg(count("*").alias("trip_count"))
                .orderBy("pickup_hour", col("trip_count").desc()))

    # Save to HDFS
    result.write.mode("overwrite").parquet(HDFS_OUTPUT_PATH)

    if __name__ == "__main__": main()