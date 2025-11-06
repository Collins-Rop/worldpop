WORLDPOP_BASE_URL = "https://data.worldpop.org/GIS/AgeSex_structures/Global_2015_2030/R2025A/2025"
GADM_BASE_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json"
RESOLUTION_PATH = "1km_ua/constrained"
CACHE_DIR = "data"
PROCESSED_DATA_FILE = "data/processed_population.parquet"
COUNTRIES = { 'KEN': 'Kenya', 'UGA': 'Uganda'}
AGE_GROUPS = ['0_4', '5_9', '10_14', '15_19', '20_24', '25_29','30_34', '35_39', '40_44', '45_49', '50_54', '55_59','60_64', '65_69', '70_74', '75_79', '80_plus']
SEX_CATEGORIES = ['M', 'F']
AGE_GROUP_LABELS = {
    '0_4': '0-4 years',
    '5_9': '5-9 years',
    '10_14': '10-14 years',
    '15_19': '15-19 years',
    '20_24': '20-24 years',
    '25_29': '25-29 years',
    '30_34': '30-34 years',
    '35_39': '35-39 years',
    '40_44': '40-44 years',
    '45_49': '45-49 years',
    '50_54': '50-54 years',
    '55_59': '55-59 years',
    '60_64': '60-64 years',
    '65_69': '65-69 years',
    '70_74': '70-74 years',
    '75_79': '75-79 years',
    '80_plus': '80+ years'
}
WORLDPOP_AGE_MAPPING = {
    '0_4': '00',
    '5_9': '05',
    '10_14': '10',
    '15_19': '15',
    '20_24': '20',
    '25_29': '25',
    '30_34': '30',
    '35_39': '35',
    '40_44': '40',
    '45_49': '45',
    '50_54': '50',
    '55_59': '55',
    '60_64': '60',
    '65_69': '65',
    '70_74': '70',
    '75_79': '75',
    '80_plus': '80'
}

HEALTH_CATEGORIES = {
    'Children (0-14)': ['0_4', '5_9', '10_14'],
    'Youth (15-24)': ['15_19', '20_24'],
    'Working Age (25-59)': ['25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59'],
    'Elderly (60+)': ['60_64', '65_69', '70_74', '75_79', '80_plus']
}