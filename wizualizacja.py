import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Wczytaj dane z pliku Excel
file_path = 'przyk1.csv'  # Zastąp ścieżkę do swojego pliku
df = pd.read_csv(file_path)

# Przekształć dane do formatu geopandas
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Wczytaj mapę świata
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Twórz wykres
fig, ax = plt.subplots(figsize=(15, 10))    
world.plot(ax=ax, color='lightgray')

# Dodaj punkty lotów na mapie
gdf.plot(ax=ax, color='red', markersize=5)

# Dostosuj wygląd wykresu
plt.title('Flight Paths Visualization')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

# Pokaż mapę
plt.show()
