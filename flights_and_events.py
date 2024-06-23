import pandas as pd

# Konwersja współrzędnych z formatu stopnie minuty sekundy do stopni dziesiętnych
def dms_to_dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
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

# Otwieranie pierwszego pliku CSV i filtrowanie danych
df1 = pd.read_csv('./states_2020-05-25-00.csv')
df1_filtered = df1[df1.apply(lambda row: in_square(row['lat'], row['lon'], lat1, lon1, lat2, lon2), axis=1)]

# Wypisywanie unikalnych wartości z kolumny 'callsign'
unique_callsigns = df1_filtered['callsign'].dropna().unique()
print("Unikalne callsigns z pliku 1:")
for callsign in unique_callsigns:
    print(callsign)

# Otwieranie drugiego pliku CSV bez nagłówków i filtrowanie danych
try:
    # Wczytaj plik CSV używając tabulatora jako separatora
    df2 = pd.read_csv('./20200525.export.CSV', delimiter='\t', on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error parsing CSV file: {e}")


# Sprawdzanie i filtrowanie danych dla kolumn 39 (lat), 40 (lon), 12 (event type) i 43 (country)
df2_filtered = df2[df2.apply(lambda row: in_square(row[53], row[54], lat1, lon1, lat2, lon2), axis=1)]

# Wypisywanie wartości z kolumn 12 (event type) i 43 (country)
print("\nEvent type i country z pliku 2:")
for index, row in df2_filtered.iterrows():
    print(f"Event type: {row[12]}, Country: {row[50]}")
