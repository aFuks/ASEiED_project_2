import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

# Definiowanie granic kontynentów i ich centrów
continents = {
    "Africa": (Polygon([(-17.625, 37.25), (-17.625, -35.0), (51.25, -35.0), (51.25, 37.25)]), Point(20, 0)),
    "Asia": (Polygon([(51.25, 81.0), (51.25, 1.0), (146.25, 1.0), (146.25, 81.0)]), Point(100, 60)),
    "Europe": (Polygon([(-31.25, 81.0), (-31.25, 35.0), (51.25, 35.0), (51.25, 81.0)]), Point(10, 50)),
    "North America": (Polygon([(-169.25, 83.0), (-169.25, 6.0), (-25.0, 6.0), (-25.0, 83.0)]), Point(-100, 40)),
    "South America": (Polygon([(-81.25, 13.0), (-81.25, -56.0), (-34.75, -56.0), (-34.75, 13.0)]), Point(-60, -20)),
    "Oceania": (Polygon([(110.0, -47.5), (110.0, 0.0), (180.0, 0.0), (180.0, -47.5)]), Point(140, -25)),
    "Antarctica": (Polygon([(-180.0, -60.0), (-180.0, -90.0), (180.0, -90.0), (180.0, -60.0)]), Point(0, -75))
}

def assign_continent(point):
    closest_continent = None
    min_distance = float('inf')
    for continent, (polygon, center) in continents.items():
        if polygon.contains(point):
            return continent
        distance = point.distance(center)
        if distance < min_distance:
            min_distance = distance
            closest_continent = continent
    return closest_continent

# Wczytaj dane z pliku CSV
file_path = 'przyk1.csv'  # Zastąp ścieżkę do swojego pliku
df = pd.read_csv(file_path, on_bad_lines='skip')

# Przekształć dane do formatu geopandas
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Dodaj kolumnę z nazwą kontynentu
gdf['continent'] = gdf['geometry'].apply(assign_continent)

# Policz liczbę lotów nad poszczególnymi kontynentami
flight_counts = gdf['continent'].value_counts()

# Wygeneruj wykres słupkowy
plt.figure(figsize=(12, 8))
flight_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Flights by Continent')
plt.xlabel('Continent')
plt.ylabel('Number of Flights')
plt.xticks(rotation=45)
plt.grid(True)

# Pokaż wykres
plt.tight_layout()
plt.show()

# Wykres kolowy pyk
plt.figure(figsize=(12,8))
flight_counts.plot(kind='pie', autopct='%1.1f%%', colors=plt.cm.Paired(range(len(flight_counts))))
plt.title('Percentage of Flights by Continent')
plt.ylabel('')

plt.tight_layout()
plt.show()
