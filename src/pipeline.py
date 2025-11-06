import os
import pandas as pd
from typing import List, Dict
from pathlib import Path
import sys

sys.path.append(os.path.dirname(__file__))
from config import *
from utils import (download_file, get_raster_url, read_raster_sum, download_admin_boundaries)

class WorldPopPipeline:
    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def download_raster(self, country_code: str, sex:str, age_group: str) -> str:
        url = get_raster_url(country_code, sex, age_group, WORLDPOP_BASE_URL, RESOLUTION_PATH)
        filename = f"{country_code}_{sex}_{age_group}.tif"
        cache_path = os.path.join(self.cache_dir, 'rasters', filename)
        success = download_file(url, cache_path)

        return cache_path if success else ""
    
    def process_country_data(self, country_code: str) -> pd.DataFrame:
        print(f"\n{'='*60}")
        print(f"Processing {COUNTRIES[country_code]} ({country_code})")
        print(f"{'='*60}")

        results = []
        for sex in SEX_CATEGORIES:
            for age_group in AGE_GROUPS:
                print(f"Processing: {sex} {age_group}...", end='')
                raster_path = self.download_raster(country_code, sex, age_group)
                if raster_path and os.path.exists(raster_path):
                    population = read_raster_sum(raster_path)
                    results.append({
                        'country_code': country_code,
                        'country_name': COUNTRIES[country_code],
                        'sex': sex,
                        'sex_label': "Male" if sex == "M" else "Female",
                        'age_group': age_group,
                        'age_group_label': AGE_GROUP_LABELS[age_group],
                        'population': population
                    })
                    print(f" Done. Population: {population:,.0f}")
                else:
                    print(" Failed to download raster.")
        return pd.DataFrame(results)
    
    def process_all_countries(self) -> pd.DataFrame:
        all_data = []
        for country_code in COUNTRIES.keys():
            df = self.process_country_data(country_code)
            all_data.append(df)
        combined_df = pd.concat(all_data, ignore_index=True)
        age_order = {age: idx for idx, age in enumerate(AGE_GROUPS)}
        combined_df['age_order'] = combined_df['age_group'].map(age_order)
        
        return combined_df
    
    def save_processed_data(self, df: pd.DataFrame, output_path: str = PROCESSED_DATA_FILE):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_parquet(output_path, index=False)
        print(f"\n{'='*60}")
        print(f"Processed data saved to {output_path}")
        print(f"Total records: {len(df):,}")
        print(f"Total population: {df['population'].sum():,.0f}")
        print(f"{'='*60}\n")

    def run(self):
        print("\n" + "="*60)
        print("WORLDPOP DATA PIPELINE")
        print("="*60)
        print(f"Countries: {', '.join(COUNTRIES.values())}")
        print(f"Age groups: {len(AGE_GROUPS)}")
        print(f"Sex categories: {len(SEX_CATEGORIES)}")
        print(f"Total files to process: {len(COUNTRIES) * len(AGE_GROUPS) * len(SEX_CATEGORIES)}")
        print("="*60 + "\n")

        df = self.process_all_countries()
        self.save_processed_data(df)

        self.print_summary(df)
        return df
    
    def print_summary(self, df: pd.DataFrame):
        print("\n" + "="*60)
        print("DATA SUMMARY")
        print("="*60)
        
        for country_code in COUNTRIES.keys():
            country_data = df[df['country_code'] == country_code]
            country_name = COUNTRIES[country_code]
            total_pop = country_data['population'].sum()
            male_pop = country_data[country_data['sex'] == 'M']['population'].sum()
            female_pop = country_data[country_data['sex'] == 'F']['population'].sum()
            
            print(f"\n{country_name}:")
            print(f"  Total Population: {total_pop:,.0f}")
            print(f"  Male: {male_pop:,.0f} ({male_pop/total_pop*100:.1f}%)")
            print(f"  Female: {female_pop:,.0f} ({female_pop/total_pop*100:.1f}%)")

        print("\n" + "="*60 + "\n")

def main():
    pipeline = WorldPopPipeline()
    pipeline.run()

if __name__ == "__main__":
    main()