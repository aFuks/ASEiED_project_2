from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_date
import pandas as pd
import matplotlib.pyplot as plt
import boto3

S3_DATA_SOURCE_PATH = 's3://lotydane/data-source/'
S3_DATA_OUTPUT_PATH = 's3://lotydane/output/flights_to_ATL.csv'
S3_PLOT_OUTPUT_PATH = 's3://lotydane/output/flights_to_ATL.png'

def main():
    spark = SparkSession.builder.appName("FlightDataAnalysis").getOrCreate()
    df = spark.read.csv(S3_DATA_SOURCE_PATH, header=True, inferSchema=True)
    df.printSchema()
    df = df.withColumn("timestamp", (df["time"]).cast("timestamp"))
    df = df.withColumn("date", to_date(col("timestamp")))

    # Define the coordinates for ATL
    atl_lat = 33.6407
    atl_lon = -84.4277
    threshold = 0.1  
    df_atl = df.where((abs(col("lat") - atl_lat) <= threshold) & (abs(col("lon") - atl_lon) <= threshold))
    spill_date = "2010-04-20"
    df_before = df_atl.where(col("date") < lit(spill_date))
    df_after = df_atl.where(col("date") >= lit(spill_date))

    daily_flights_before = df_before.groupBy("date").count().orderBy("date")
    daily_flights_after = df_after.groupBy("date").count().orderBy("date")

    daily_flights_before.show()
    daily_flights_after.show()

    daily_flights_before_pd = daily_flights_before.toPandas()
    daily_flights_after_pd = daily_flights_after.toPandas()

    plt.figure(figsize=(12, 6))
    plt.plot(daily_flights_before_pd['date'], daily_flights_before_pd['count'], label='Before Spill', marker='o')
    plt.plot(daily_flights_after_pd['date'], daily_flights_after_pd['count'], label='After Spill', marker='o')
    plt.title('Number of Flights to ATL Before and After Deepwater Horizon Spill')
    plt.xlabel('Date')
    plt.ylabel('Number of Flights')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("/tmp/flights_to_ATL.png")
    plt.show()

    combined_df = daily_flights_before.union(daily_flights_after)
    combined_df.write.mode('overwrite').csv(S3_DATA_OUTPUT_PATH, header=True)

    s3 = boto3.client('s3')
    s3.upload_file('/tmp/flights_to_ATL.png', 'lotydane', 'output/flights_to_ATL.png')

    spark.stop()

if __name__ == "__main__":
    main()
