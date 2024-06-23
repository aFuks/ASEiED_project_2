import os
import requests
import zipfile
from datetime import datetime, timedelta

base_url = "http://data.gdeltproject.org/events/"
start_date = datetime.strptime("20200525", "%Y%m%d")
end_date = datetime.strptime("20220627", "%Y%m%d")
output_folder = "Events"

os.makedirs(output_folder, exist_ok=True)

date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
file_names = [date.strftime("%Y%m%d") + ".export.CSV.zip" for date in date_list]

for file_name in file_names:
    url = base_url + file_name
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        zip_path = os.path.join(output_folder, file_name)
        with open(zip_path, 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        os.remove(zip_path)
    else:
        print(f"Plik {file_name} nie został znaleziony na serwerze.")

print("Proces zakończony.")
