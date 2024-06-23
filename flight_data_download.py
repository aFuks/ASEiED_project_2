import requests
import tarfile
import os
import gzip
import shutil
import pandas as pd
from datetime import datetime, timedelta

def download_data(url, tar_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(tar_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Plik został pobrany i zapisany w {tar_path}")
    else:
        print(f"Błąd pobierania pliku: {response.status_code}")

    # Rozpakuj plik tar
    if tarfile.is_tarfile(tar_path):
        with tarfile.open(tar_path) as tar:
            tar.extractall(path='data')
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('.gz'):
                    gz_path = os.path.join('data', member.name)
                    print(f"Plik został rozpakowany: {gz_path}")
                    # Rozpakuj plik gz
                    csv_path = gz_path.replace('.gz', '')
                    with gzip.open(gz_path, 'rb') as f_in:
                        with open(csv_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    print(f"Plik gz został rozpakowany do: {csv_path}")
                    # Usuń plik gz po rozpakowaniu
                    os.remove(gz_path)
    else:
        print("Plik nie jest prawidłowym plikiem tar")

    # Usuń plik tar po rozpakowaniu
    os.remove(tar_path)

# Funkcja do generowania dat co 7 dni
def generate_dates(start_date, end_date):
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=7)
    return dates


if not os.path.exists('data'):
    os.makedirs('data')


# Podaj pierwszą i ostatnią datę
start_date = datetime(2022, 6, 13)
end_date = datetime(2022, 6, 27)

dates = generate_dates(start_date, end_date)

for date in dates:
    date_str = date.strftime('%Y-%m-%d')
    for i in range(24):
        hour_str = f"{i:02d}"
        url = f"https://opensky-network.org/datasets/states/{date_str}/{hour_str}/states_{date_str}-{hour_str}.csv.tar"
        tar_path = os.path.join('data', f'states_{date_str}-{hour_str}.csv.tar')
        download_data(url, tar_path)
