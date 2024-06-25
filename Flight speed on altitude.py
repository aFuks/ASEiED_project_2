from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Inicjalizacja sesji Spark
    spark = SparkSession.builder.appName("FlightDataAnalysis").getOrCreate()
    folder_path = "loty"
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    df = spark.read.csv(all_files, header=True, inferSchema=True)
    df.printSchema()
    df = df.withColumn("timestamp", (df["time"]).cast("timestamp"))
    df.createOrReplaceTempView("flights")

    daily_flights_query = """
        SELECT
            DATE(timestamp) as date,
            COUNT(*) as flight_count
        FROM flights
        GROUP BY DATE(timestamp)
        ORDER BY date
    """
    daily_flights = spark.sql(daily_flights_query)
    daily_flights.show()

    # Wizualizacja liczby lotów w ciągu dnia
    daily_flights_pd = daily_flights.toPandas()
    plt.figure(figsize=(12, 6))
    plt.plot(daily_flights_pd['date'], daily_flights_pd['flight_count'], marker='o')
    plt.title('Number of Flights per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Flights')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("flights_per_day.png")
    plt.show()

    # Analiza prędkości i wysokości lotów
    speed_altitude_query = """
        SELECT
            velocity,
            baroaltitude
        FROM flights
        WHERE velocity IS NOT NULL AND baroaltitude IS NOT NULL
    """
    speed_altitude = spark.sql(speed_altitude_query)
    speed_altitude.show()

    # Wizualizacja zależności między prędkością a wysokością lotów
    speed_altitude_pd = speed_altitude.toPandas()
    plt.figure(figsize=(10, 6))
    plt.scatter(speed_altitude_pd['velocity'], speed_altitude_pd['baroaltitude'], alpha=0.5)
    plt.title('Flight Speed vs. Altitude')
    plt.xlabel('Speed (m/s)')
    plt.ylabel('Altitude (m)')
    plt.tight_layout()
    plt.savefig("speed_vs_altitude.png")
    plt.show()

    # Analiza liczby lotów na wybranych trasach
    top_routes_query = """
        SELECT
            icao24 AS origin,
            callsign AS destination,
            COUNT(*) as flight_count
        FROM flights
        WHERE icao24 IS NOT NULL AND callsign IS NOT NULL
        GROUP BY icao24, callsign
        ORDER BY flight_count DESC
        LIMIT 10
    """
    top_routes = spark.sql(top_routes_query)
    top_routes.show()

    # Wizualizacja liczby lotów na wybranych trasach
    top_routes_pd = top_routes.toPandas()
    plt.figure(figsize=(10, 6))
    top_routes_pd.plot(kind='bar', x='origin', y='flight_count', legend=False)
    plt.title('Top 10 Routes by Number of Flights')
    plt.xlabel('Routes')
    plt.ylabel('Number of Flights')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_routes.png")
    plt.show()

    # Zakończenie sesji Spark
    spark.stop()

if __name__ == "__main__":
    main()