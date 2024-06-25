import pandas as pd
import matplotlib.pyplot as plt
import glob
from geopy.distance import great_circle

# Współrzędne lotnisk w stolicach Europy
airports = {
    "Warsaw": [(52.1657, 20.9671)],  # Lotnisko Chopina
    "Berlin": [(52.3667, 13.5033), (52.5597, 13.2877)],  # Brandenburg, Tegel (zamknięte, ale dodane dla przykładu)
    "London": [(51.4700, -0.4543), (51.8963, 0.0759), (51.1537, -0.1821)],  # Heathrow, Stansted, Gatwick
    "Paris": [(49.0097, 2.5479), (48.7253, 2.3592)],  # Charles de Gaulle, Orly
    "Madrid": [(40.4983, -3.5676)],  # Barajas
    "Rome": [(41.8003, 12.2389), (41.7999, 12.5949)],  # Fiumicino, Ciampino
    # Dodaj więcej lotnisk w miarę potrzeby
}

# Funkcja sprawdzająca, czy samolot jest w pobliżu lotniska
def is_near_any_airport(lat, lon, airport_coords_list, radius=100):
    return any(great_circle((lat, lon), coords).km <= radius for coords in airport_coords_list)

# Ścieżka do plików CSV
file_pattern = 'data/states_*-*-*-12.csv'
files = sorted(glob.glob(file_pattern))

# Przechowywanie wyników
results = {city: [] for city in airports}
dates = []

# Analiza danych
for file in files:
    print(f'Processing file: {file}')
    seen_aircraft = {city: set() for city in airports}
    chunksize = 100000  # Wczytywanie danych w kawałkach po 100000 wierszy

    for chunk in pd.read_csv(file, chunksize=chunksize):
        chunk = chunk.dropna(subset=['lat', 'lon', 'icao24'])  # Usuwanie wierszy z brakującymi danymi
        for index, row in chunk.iterrows():
            for city, coords_list in airports.items():
                if row['icao24'] not in seen_aircraft[city] and is_near_any_airport(row['lat'], row['lon'], coords_list):
                    seen_aircraft[city].add(row['icao24'])

    for city in airports:
        results[city].append(len(seen_aircraft[city]))

    # Extract the date from the filename
    date_str = file.split('_')[1]  # assuming filename format is states_YYYY-MM-DD-HH.csv
    dates.append(date_str)

# Generowanie wykresów
plt.figure(figsize=(14, 8))
for city, counts in results.items():
    plt.plot(dates, counts, label=city)

plt.title('Number of planes near airports in European capitals over time')
plt.xlabel('Date')
plt.ylabel('Number of planes')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('planes_near_capitals.png')
plt.show()
