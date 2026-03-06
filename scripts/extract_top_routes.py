#!/usr/bin/env python3
# Data Engineering I - Result Extraction Script

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number

def main():
    # Initialize the Spark session
    spark = SparkSession.builder.appName("ExtractTopRoutes").getOrCreate()

    # Load the processed results from HDFS
    print("Loading data from HDFS...")
    df = spark.read.load("/output/avg_trip_time")
    
    # Define the window specification to rank by trip count per hour
    windowSpec = Window.partitionBy("time_stamp").orderBy(col("trip_count").desc())

    # PART 1: Raw Data (Including unknown zones 264/265) 
    print("\n=== Top Routes Per Hour (Raw Data / Unfiltered) ===")
    all_routes = df.withColumn("rank", row_number().over(windowSpec)) \
                   .filter(col("rank") == 1) \
                   .drop("rank") \
                   .orderBy(col("time_stamp").cast("int"))
    all_routes.show(24, truncate=False)

    # PART 2: Cleaned Data (Excluding unknown zones) 
    print("\n=== True Top Routes Per Hour (Filtered / Real Zones) ===")
    # Filter out trips starting or ending in unknown zones (264 and 265)
    df_clean = df.filter(~col("route").contains("264") & ~col("route").contains("265"))
    
    # Extract the true top route for each hour
    real_top_routes = df_clean.withColumn("rank", row_number().over(windowSpec)) \
                              .filter(col("rank") == 1) \
                              .drop("rank") \
                              .orderBy(col("time_stamp").cast("int"))
    real_top_routes.show(24, truncate=False)

    # Stop the Spark session to release resources
    spark.stop()

if __name__ == "__main__":
    main()
