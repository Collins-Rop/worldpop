import os
import requests
from typing import Dict, List, Optional
import geopandas as gpd
import rasterio
import numpy as np
from pathlib import Path

def download_file(url: str, output_path: str, force: bool = False) -> bool:
    if os.path.exists(output_path) and not force:
        print(f"File {output_path} already exists.")
        return True
    try:
        print(f"Downloading {url} to {output_path}...")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {output_path} successfully.")
        return True
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
        return False
    
def get_raster_url(country_code: str, sex: str, age_group: str, base_url: str, resolution_path: str) -> str:
    from config import WORLDPOP_AGE_MAPPING
    age_code = WORLDPOP_AGE_MAPPING.get(age_group, age_group)
    country_lower = country_code.lower()
    sex_lower = sex.lower()
    filename = f"{country_lower}_{sex_lower}_{age_code}_2025_CN_1km_R2025A_UA_v1.tif"
    url = f"{base_url}/{country_code}/v1/{resolution_path}/{filename}"
    return url

def read_raster_sum(file_path: str) -> float:
    try:
        with rasterio.open(file_path) as src:
            data = src.read(1)
            data = np.where(data == src.nodata, 0, data)
            total = np.sum(data)
        return total
    except Exception as e:
        print(f"Error reading raster file {file_path}: {e}")
        return 0.0
    
def download_admin_boundaries(country_code: str, level: int, base_url: str, cache_dir: str) -> Optional[gpd.GeoDataFrame]:
    filename = f"gadm41_{country_code}_{level}.json"
    zip_url = f"{base_url}/{filename}.zip"
    cache_path = os.path.join(cache_dir, f"{country_code}_admin{level}.geojson")
    if os.path.exists(cache_path):
        print(f"Loading cached boundaries: {cache_path}")
        return gpd.read_file(cache_path)
    try:
        import zipfile
        import io
        
        print(f"Downloading boundaries: {zip_url}")
        response = requests.get(zip_url, timeout=60)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(os.path.join(cache_dir, 'temp'))
        
        json_path = os.path.join(cache_dir, 'temp', filename)
        gdf = gpd.read_file(json_path)
        os.makedirs(cache_dir, exist_ok=True)
        gdf.to_file(cache_path, driver='GeoJSON')
        
        print(f"Cached boundaries: {cache_path}")
        return gdf
    except Exception as e:
        print(f"Error downloading boundaries: {e}")
        return None
    
def calculate_health_indicators(df) -> Dict[str, float]:
    total_pop = df['population'].sum()
    if total_pop == 0:
        return {}
    indicators = {}
    children_ages = ['0_4', '5_9', '10_14']
    youth_ages = ['15_19', '20_24']
    working_ages = ['25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59']
    elderly_ages = ['60_64', '65_69', '70_74', '75_79', '80_plus']
    children_pop = df[df['age_group'].isin(children_ages)]['population'].sum()
    youth_pop = df[df['age_group'].isin(youth_ages)]['population'].sum()
    working_pop = df[df['age_group'].isin(working_ages)]['population'].sum()
    elderly_pop = df[df['age_group'].isin(elderly_ages)]['population'].sum()
    indicators['children_pct'] = (children_pop / total_pop * 100) if total_pop > 0 else 0
    indicators['youth_pct'] = (youth_pop / total_pop * 100) if total_pop > 0 else 0
    indicators['working_age_pct'] = (working_pop / total_pop * 100) if total_pop > 0 else 0
    indicators['elderly_pct'] = (elderly_pop / total_pop * 100) if total_pop > 0 else 0
    if working_pop > 0:
        indicators['dependency_ratio'] = (children_pop + elderly_pop) / working_pop * 100

    male_pop = df[df['sex'] == 'M']['population'].sum()
    female_pop = df[df['sex'] == 'F']['population'].sum()
    if female_pop > 0:
        indicators['sex_ratio'] = (male_pop / female_pop) * 100

    return indicators