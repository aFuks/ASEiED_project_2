import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

# Definicja lotnisk i ich współrzędnych
airports = {
    'LHR': {'name': 'London Heathrow', 'coords': (51.4700, -0.4543)},
    'DXB': {'name': 'Dubai International', 'coords': (25.2532, 55.3657)},
    'ATL': {'name': 'Hartsfield-Jackson Atlanta International', 'coords': (33.6407, -84.4277)},
}

# Funkcja do wczytywania wszystkich plików CSV z folderu
def load_all_csv_from_folder(folder):
    all_files = glob.glob(os.path.join(folder, "*.csv"))
    df_list = [pd.read_csv(file) for file in all_files]
    return pd.concat(df_list, ignore_index=True)

# Funkcja do filtrowania samolotów na ziemi na danym lotnisku
def filter_aircrafts_on_ground(df, coords, radius):
    lat, lon = coords
    filtered_df = df[(df['onground'] == True) & 
                     (df['lat'].between(lat - radius, lat + radius)) & 
                     (df['lon'].between(lon - radius, lon + radius))]
    return filtered_df

# Wczytywanie danych z plików CSV
folder = 'data'
data = load_all_csv_from_folder(folder)

# Funkcja do wyświetlania trendów odlotów
def plot_departure_trends(data, airports):
    plt.figure(figsize=(14, 8))
    for airport_code, details in airports.items():
        airport_name = details['name']
        airport_coords = details['coords']
        
        # Filtracja samolotów na ziemi
        if airport_code=='DXB':
            radius=0.01 # w Dubaju dużo lotnisk blisko siebie
        else:
            radius=1
        on_ground_df = filter_aircrafts_on_ground(data, airport_coords, radius)
        on_ground_df['hour'] = pd.to_datetime(on_ground_df['time'], unit='s').dt.hour
        departures_by_hour = on_ground_df.groupby('hour')['icao24'].nunique()
        
        plt.plot(departures_by_hour.index, departures_by_hour, label=airport_name)
        
        # Dodanie etykiet danych
        for hour, count in departures_by_hour.items():
            plt.text(hour, count, str(count), fontsize=9, ha='center', va='bottom')
    
    plt.title('Liczba odlotów na godzinę z różnych lotnisk')
    plt.xlabel('Godzina')
    plt.ylabel('Liczba odlotów')
    plt.legend()
    plt.grid(True)
    plt.show()

# Wyświetlenie trendów odlotów
plot_departure_trends(data, airports)
