from pyspark.sql.functions import hour, col, concat, lit

def load_and_filter(spark, input_path):
    df = spark.read.parquet(input_path)

    #Removes all trips with a distance of 0
    df = df.filter(col("trip_distance") > 0)
    #Remove all unknown zones
    df = df.filter((col("PULocationID") != 264) & (col("PULocationID") != 265))
    df = df.filter((col("DOLocationID") != 264) & (col("DOLocationID") != 265))
    #Get the hour from the datetime
    df = df.withColumn("time_stamp",hour(col("tpep_pickup_datetime")))
    #Create column with route
    df = df.withColumn("route",
        concat(col("PULocationID").cast("string"),
            lit(" to "),
            col("DOLocationID").cast("string")))
    #Only keep relevant columns
    df = df.select("time_stamp", "route")

    return df
