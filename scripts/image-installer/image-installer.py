import pandas as pd
import os
import requests
from tqdm import tqdm

# Replace with your download location
download_loc = "/Volumes/MyPassport/Data"
# Replace with your Results Export from NRCAN OpenData SAR RADSAT1 Search 
csv_file_path = "Results.csv"

dataframe = pd.read_csv(csv_file_path)

for index, row in dataframe.iterrows():
    file_url = row['Download Link']
    file_name = os.path.join(download_loc, os.path.basename(file_url))
    
    print(f"Downloading {file_name}...")
    
    response = requests.get(file_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    
    with open(file_name, 'wb') as file, tqdm(
        desc=file_name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)
    
    print(f"Downloaded {file_name}")
    print(f"File {index + 1} out of {len(dataframe)} downloaded.")