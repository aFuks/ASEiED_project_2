from pyspark.sql import SparkSession
from pyspark.sql.functions import col

S3_DATA_SOURCE_PATH = 's3://lotydane/data-source/'
S3_DATA_OUTPUT_PATH = 's3://lotydane/output/'

def filter(inputpath,min_lat,max_lat,min_lon,max_lon,spark,outputpath):
    selected_data=[]
    for i in range(24):
        file_path = inputpath.format(i)
        alldata = spark.read.csv(file_path, header=True)
        selected_data.append=alldata.where((col("lat") >= min_lat) & (col("lat") <= max_lat) &
        (col("lon") >= min_lon) & (col("lon") <= max_lon))
    combined_data = selected_data[0]
    for df in selected_data[1:]:
        combined_data = combined_data.union(df)
    combined_data.coalesce(1).write.mode('overwrite').csv(outputpath,header=True)
def main():
    spark = SparkSession.builder.appName('flightfilter').getOrCreate()

    filter( f"{S3_DATA_SOURCE_PATH}/states_2020-06-29-{{:02d}}.csv",52.148307723339485, 52.18238951601168,
           20.941468608732215,20.98738649910821,spark,f"{S3_DATA_OUTPUT_PATH}/warszawa") #lotnisko warszawa
    filter( f"{S3_DATA_SOURCE_PATH}/states_2021-08-30-{{:02d}}.csv",29.97873342237595, 30.010994985996863,
            -90.28570473079789, -90.24158775899534, spark,f"{S3_DATA_OUTPUT_PATH}/louisiana")  # Luizjana huragan
    filter( f"{S3_DATA_SOURCE_PATH}/states_2021-11-29-{{:02d}}.csv",-28.868352292148156, -28.439216135183663,
           -18.0222540407791, -17.680869018649712, spark,f"{S3_DATA_OUTPUT_PATH}/la_palma")  # la palma
    filter(f"{S3_DATA_SOURCE_PATH}/states_2022-02-28-{{:02d}}.csv",47.9525254824843, 52.24749063117518,
           24.04518269949129, 38.78179587580102, spark,f"{S3_DATA_OUTPUT_PATH}/ukraine")  # Cała Ukraina
if __name__ == "__main__":
    main()
