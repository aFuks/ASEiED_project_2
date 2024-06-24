import pandas as pd
import glob
import os
import folium

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
def filter_aircrafts_on_ground(df, coords, radius=0.5):
    lat, lon = coords
    filtered_df = df[(df['onground'] == True) & 
                     (df['lat'].between(lat - radius, lat + radius)) & 
                     (df['lon'].between(lon - radius, lon + radius))]
    return filtered_df

# Funkcja do nanoszenia lotów na mapę
def plot_flights_on_map(data, airports):
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    for airport_code, details in airports.items():
        airport_name = details['name']
        airport_coords = details['coords']
        
        # Filtracja samolotów, które wystartowały z danego lotniska
        on_ground_df = filter_aircrafts_on_ground(data, airport_coords)
        
        for icao24 in on_ground_df['icao24'].unique():
            aircraft_data = data[data['icao24'] == icao24]
            
            # Dodanie punktu początkowego na mapie
            folium.Marker(
                location=airport_coords,
                popup=f"{airport_name} ({airport_code})",
                icon=folium.Icon(color='green')
            ).add_to(m)
            
            # Przechowywanie współrzędnych dla lotu
            flight_path = []
            
            for _, row in aircraft_data.iterrows():
                if not row['onground']:
                    # Sprawdzanie i usuwanie NaN w danych współrzędnych
                    if not pd.isna(row['lat']) and not pd.isna(row['lon']):
                        flight_path.append((row['lat'], row['lon']))
                if row['onground'] and flight_path:
                    break
            
            # Dodanie linii lotu na mapie
            if flight_path:
                folium.PolyLine(
                    flight_path,
                    color='blue',
                    weight=2.5,
                    opacity=1
                ).add_to(m)
    
    return m

# Wczytywanie danych z plików CSV
folder = 'data1'
data = load_all_csv_from_folder(folder)

# Wyświetlenie mapy z lotami
flight_map = plot_flights_on_map(data, airports)
flight_map.save('flight_map.html')
