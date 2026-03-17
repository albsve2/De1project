'''Paths'''
HDFS_INPUT_PATH  = "hdfs:///data/taxi/*.parquet" # Dataset location
HDFS_OUTPUT_PATH = "hdfs:///output/avg_trip_time" # Output location

#FOR WEAK SCALING
""""
#2012-2013 dataset ~ 28 GB
HDFS_INPUT_PATH  = "hdfs:///data/taxi/yellow_tripdata_201[23]-*.parquet"
HDFS_OUTPUT_PATH = "hdfs:///output/run1_weak_scaling"

#2012-2015 dataset ~ 48 GB
HDFS_INPUT_PATH  = "hdfs:///data/taxi/yellow_tripdata_201[2345]-*.parquet"
HDFS_OUTPUT_PATH = "hdfs:///output/run2_weak_scaling

#2012-2017 dataset ~ 72 GB
HDFS_INPUT_PATH  = "hdfs:///data/taxi/yellow_tripdata_201[234567]-*.parquet"
HDFS_OUTPUT_PATH = "hdfs:///output/run3_weak_scaling
"""

'''Spark'''
APP_NAME         = "NYC Taxi Zone Analysis" # Name of the application
#MASTER_URL = "local[*]" #Only for master node testing
MASTER_URL       = "spark://192.168.2.53:7077" #For cluster
EXECUTOR_MEMORY  = "1g" # 1 of out of 2gb available
EXECUTOR_CORES   = "1" # 1 of out of 2 cores available
DRIVER_HOST      = "192.168.2.53" # Master node IP
