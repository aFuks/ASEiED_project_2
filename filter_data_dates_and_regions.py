from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from collections import defaultdict

S3_DATA_SOURCE_PATH = 's3://lotydane/data-source/'
S3_DATA_OUTPUT_PATH = 's3://lotydane/output/combined_output.csv'
TXT_OUTPUT_PATH = 's3://lotydane/output/combined_output_counts.txt'  # Local path for Spark cluster

def filter(inputpath, date, regions, spark):
    selected_data = []
    region_counts = defaultdict(int)  # Dictionary to store counts for each region and date combination

    for i in range(24):
        file_path = inputpath.format(i)  # Correct the formatting here
        alldata = spark.read.csv(file_path, header=True)
        for region in regions:
            region_name, min_lat, max_lat, min_lon, max_lon = region
            filtered_data = alldata.where((col("lat") >= min_lat) & (col("lat") <= max_lat) &
                                          (col("lon") >= min_lon) & (col("lon") <= max_lon))
            region_count = filtered_data.count()  # Count occurrences for the region
            region_counts[(region_name, date)] += region_count  # Update the count for the region and date
            filtered_data = filtered_data.withColumn("region", lit(region_name))
            filtered_data = filtered_data.withColumn("date", lit(date))  # Add date column
            selected_data.append(filtered_data)
            print("timestamppp")

    return selected_data, region_counts

def main():
    spark = SparkSession.builder.appName('flightfilter').getOrCreate()

    regions = [
        ("warszawa", 52.148307723339485, 52.18238951601168, 20.941468608732215, 20.98738649910821),
        ("louisiana", 29.97873342237595, 30.010994985996863, -90.28570473079789, -90.24158775899534),
        ("la_palma", 28.868352292148156, 28.439216135183663, -18.0222540407791, -17.680869018649712),
        ("ukraine", 47.9525254824843, 52.24749063117518, 24.04518269949129, 38.78179587580102)
    ]

    dates = ["2020-06-29", "2021-08-30", "2021-11-29", "2021-12-20", "2022-02-28"]

    all_selected_data = []
    all_region_counts = defaultdict(int)  # Dictionary to store counts for each region and date combination

    for date in dates:
        selected_data, region_counts = filter(f"{S3_DATA_SOURCE_PATH}/states_{date}-{{:02d}}.csv", date, regions, spark)
        all_selected_data.extend(selected_data)
        for key, count in region_counts.items():
            all_region_counts[key] += count

    if all_selected_data:
        combined_data = all_selected_data[0]
        for df in all_selected_data[1:]:
            combined_data = combined_data.union(df)
        combined_data.coalesce(1).write.mode('overwrite').csv(S3_DATA_OUTPUT_PATH, header=True)

    # Sort the counts by region and date
    sorted_counts = sorted(all_region_counts.items(), key=lambda x: (x[0][0], x[0][1]))

    # Write the counts to a text file
    with open(TXT_OUTPUT_PATH, "w") as f:
        for (region, date), count in sorted_counts:
            f.write(f"{region}, {date}: {count}\n")

    print("Completed filtering for all dates and regions.")

if __name__ == "__main__":
    main()
