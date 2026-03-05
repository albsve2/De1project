'''Paths'''
HDFS_INPUT_PATH  = "hdfs:///data/taxi/*.parquet" # Dataset location
HDFS_OUTPUT_PATH = "hdfs:///output/avg_trip_time" # Output location

'''Spark'''
APP_NAME         = "NYC Taxi Zone Analysis" # Name of the application
#MASTER_URL = "local[*]" #Only for master node testing
MASTER_URL       = "spark://192.168.2.53:7077" #For cluster
EXECUTOR_MEMORY  = "1g" # 1 of out of 2gb available
EXECUTOR_CORES   = "1" # 1 of out of 2 cores available
DRIVER_HOST      = "192.168.2.53" # Master node IP
