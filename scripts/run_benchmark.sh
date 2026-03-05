#!/bin/bash

# Data Engineering I - Project VT 2026
# Scalability Experiments Benchmark Script
# 
# NOTE TO GRADERS!!!: 
# Due to Spark's default spread-out behavior and resource limits
# hardcoded in src/config.py, passing --executor-cores via terminal was overridden.
# To guarantee strict node isolation for strong scaling, we manually restricted 
# the number of active workers between runs by editing /opt/spark/conf/workers 
# and restarting the cluster using stop-all.sh and start-all.sh.

echo "Running Horizontal Test: 1 Worker (2 Cores)"
# MANUAL PREREQUISITE: Comment out 2 workers in /opt/spark/conf/workers and restart Spark.
time spark-submit --master spark://192.168.2.53:7077 --conf spark.driver.host=192.168.2.53 --conf spark.driver.bindAddress=192.168.2.53 --py-files src/config.py,src/etl_job.py src/analysis_job.py

echo "Running Horizontal Test: 2 Workers (4 Cores)"
# MANUAL PREREQUISITE: Comment out 1 worker in /opt/spark/conf/workers and restart Spark.
time spark-submit --master spark://192.168.2.53:7077 --conf spark.driver.host=192.168.2.53 --conf spark.driver.bindAddress=192.168.2.53 --py-files src/config.py,src/etl_job.py src/analysis_job.py

echo "Running Horizontal Test: 3 Workers (6 Cores)"
# MANUAL PREREQUISITE: Ensure all 3 workers are active in /opt/spark/conf/workers and restart Spark.
time spark-submit --master spark://192.168.2.53:7077 --conf spark.driver.host=192.168.2.53 --conf spark.driver.bindAddress=192.168.2.53 --py-files src/config.py,src/etl_job.py src/analysis_job.py

echo "Running Vertical Test: 1 Worker (1 Core)"
# MANUAL PREREQUISITE: Only 1 worker active. We use flags to restrict it to 1 worker.
time spark-submit --master spark://192.168.2.53:7077 --conf spark.driver.host=192.168.2.53 --conf spark.driver.bindAddress=192.168.2.53 --executor-cores 1 --total-executor-cores 1 --py-files src/config.py,src/etl_job.py src/analysis_job.py

echo "Running Vertical Test: 2 Worker (2 Core)"
# MANUAL PREREQUISITE: 2 workers active. We use flags to restrict it to 2 workers.
time spark-submit --master spark://192.168.2.53:7077 --conf spark.driver.host=192.168.2.53 --conf spark.driver.bindAddress=192.168.2.53 --executor-cores 1 --total-executor-cores 2 --py-files src/config.py,src/etl_job.py src/analysis_job.py

echo "Running Vertical Test: 3 Worker (3 Core)"
# MANUAL PREREQUISITE: All workers active. 
time spark-submit --master spark://192.168.2.53:7077 --conf spark.driver.host=192.168.2.53 --conf spark.driver.bindAddress=192.168.2.53 --executor-cores 1 --total-executor-cores 3 --py-files src/config.py,src/etl_job.py src/analysis_job.py


echo "All benchmark commands completed!"


