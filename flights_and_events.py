import pandas as pd
from datetime import datetime

# Konwersja współrzędnych z formatu stopnie minuty sekundy do stopni dziesiętnych
def dms_to_dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction in ['S', 'W']:
        dd *= -1
    return dd

# Współrzędne narożników kwadratu
lat1 = dms_to_dd(43, 48, 25.3, 'N')
lon1 = dms_to_dd(39, 42, 37.3, 'E')
lat2 = dms_to_dd(38, 22, 36.1, 'N')
lon2 = dms_to_dd(49, 45, 27.4, 'E')

# Funkcja do sprawdzenia, czy współrzędne są w kwadracie
def in_square(lat, lon, lat1, lon1, lat2, lon2):
    return lat2 <= lat <= lat1 and lon1 <= lon <= lon2

# Sprawdzanie dostępnych kolumn w pliku CSV
def print_columns(file_path, delimiter=','):
    try:
        df = pd.read_csv(file_path, delimiter=delimiter, on_bad_lines='skip', engine='python')
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Wypisz kolumny z plików CSV, aby sprawdzić, jakie kolumny są dostępne
flight_files = ['./states_2020-05-25-00.csv', './states_2022-06-27-00.csv']  # Dodaj wszystkie pliki lotów tutaj
event_files = ['./20200525.export.CSV', './20220627.export.CSV']  # Dodaj wszystkie pliki wydarzeń tutaj


# Otwieranie plików CSV z danymi o lotach i filtrowanie danych
df_flights_list = []

for file in flight_files:
    df_flights = pd.read_csv(file)
    # Konwersja kolumny 'time' z sekund od 1.1.1970 do daty i czasu
    df_flights['timestamp'] = pd.to_datetime(df_flights['time'], unit='s')

    df_flights_filtered = df_flights[df_flights.apply(lambda row: in_square(row['lat'], row['lon'], lat1, lon1, lat2, lon2), axis=1)]
    df_flights_list.append(df_flights_filtered)

df_flights_combined = pd.concat(df_flights_list)

# Obliczanie średniej liczby wystąpień callsign dla każdego dnia
df_flights_combined['date'] = df_flights_combined['timestamp'].dt.date
callsign_counts = df_flights_combined.groupby('date')['callsign'].count()
average_callsign_count = callsign_counts.mean()

# Znajdowanie dni, w których liczba lotów była poniżej średniej
below_average_days = callsign_counts[callsign_counts < average_callsign_count].index

# Otwieranie plików CSV z wydarzeniami i filtrowanie danych
df_events_list = []

for file in event_files:
    try:
        df_events = pd.read_csv(file, delimiter='\t', header=None, on_bad_lines='skip', engine='python')
        # Konwersja kolumny z datą (indeks 1) do formatu daty
        df_events['date'] = pd.to_datetime(df_events[1], format='%Y%m%d', errors='coerce').dt.date
        df_events_filtered = df_events[df_events.apply(lambda row: in_square(row[39], row[40], lat1, lon1, lat2, lon2), axis=1)]
        df_events_list.append(df_events_filtered)
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

df_events_combined = pd.concat(df_events_list, ignore_index=True)

# Filtrowanie wydarzeń dla dni poniżej średniej liczby lotów
events_below_average = df_events_combined[df_events_combined['date'].isin(below_average_days)]

# Wypisywanie wyników
print("\nDni z liczbą lotów poniżej średniej i odpowiadające wydarzenia:")
for day in below_average_days:
    print(f"\nDzień: {day}")
    print(f"Liczba lotów: {callsign_counts[day]}")
    events_on_day = events_below_average[events_below_average['date'] == day]
    for index, row in events_on_day.iterrows():
        try:
            if pd.notna(row[12]):  # Sprawdź, czy 'event type' nie jest NaN
                print(f"Event type: {row[12]}, Country: {row[43]}, Date: {row['date']}")
        except IndexError:
            print(f"Brak danych w wierszu: {row}")
