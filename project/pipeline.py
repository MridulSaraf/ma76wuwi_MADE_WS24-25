import os
import pandas as pd
import sqlite3


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "project_data.db")

os.makedirs(DATA_DIR, exist_ok=True)
print(f"Data directory created or already exists at {DATA_DIR}")

# Correcting raw URLs
ev_data_url = "https://raw.githubusercontent.com/MridulSaraf/Data4MADE/main/IEA-EV-dataEV%20salesHistoricalCars.csv"
emissions_data_url = "https://raw.githubusercontent.com/MridulSaraf/Data4MADE/main/b61929c4-3c0f-4ab6-ae58-6ab62624d304_Data.csv"


os.makedirs(DATA_DIR, exist_ok=True)

def load_data(file_path):
    """Loads data from the provided file path."""
    try:
        df = pd.read_csv(file_path, delimiter=',', on_bad_lines='skip', engine='python')
        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def clean_transform_ev_data(df):
    """Cleans and transforms EV data."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.ffill(inplace=True)  
    return df

def clean_transform_emissions_data(df):
    """Cleans and transforms emissions data."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.ffill(inplace=True)
    region_mapping = {
        "usa": "united states"
    }
    df['region'] = df['region'].replace(region_mapping)
    if 'year' not in df.columns:
        raise KeyError("'year' column missing in EV data")
    return df
def clean_transform_emissions_data(df):
    """Cleans and transforms emissions data."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.ffill(inplace=True)

    # Rename 'country_name' to 'region' 
    if 'country_name' in df.columns:
        df.rename(columns={'country_name': 'region'}, inplace=True)

    # Filter out irrelevant rows based on region
    if 'region' in df.columns:
        valid_regions = df['region'].dropna().unique().tolist()
        valid_regions = [region.lower() for region in valid_regions if "world" not in region and "updated" not in region]
        df = df[df['region'].str.lower().isin(valid_regions)]

    # Identify year columns
    year_columns = [col for col in df.columns if col.startswith('20')]
    if year_columns:
        df = df.melt(id_vars=['region'], 
                     value_vars=year_columns, 
                     var_name='year', 
                     value_name='emission_value')
        df['year'] = df['year'].str.extract('(\\d{4})').astype(int)
        # Filter rows with valid numeric emission values
        df = df[pd.to_numeric(df['emission_value'], errors='coerce').notnull()]
        df['emission_value'] = df['emission_value'].astype(float)
    else:
        print("Warning: Year columns are missing or incorrectly named in the emissions data.")
        df = pd.DataFrame(columns=['region', 'year', 'emission_value'])

    return df

def save_to_database(df, table_name):
    """Saves DataFrame to SQLite database."""
    try:
        print(f"Attempting to write table '{table_name}' to database at {DB_PATH}")
        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Successfully wrote table '{table_name}' to database.")
    except Exception as e:
        print(f"Error writing to database: {e}")
        raise

def main():
    # Load datasets
    ev_data = load_data(ev_data_url)
    emissions_data = load_data(emissions_data_url)

    # Perform EDA on raw data
    print("\n--- EDA on Raw EV Data ---")
    print(ev_data.info())
    print(ev_data.describe())
    print("\n--- EDA on Raw Emissions Data ---")
    print(emissions_data.info())
    print(emissions_data.describe())

    # Clean and transform datasets
    ev_data = clean_transform_ev_data(ev_data)
    emissions_data = clean_transform_emissions_data(emissions_data)

    # Perform EDA on cleaned data
    print("\n--- EDA on Cleaned EV Data ---")
    print(ev_data.info())
    print(ev_data.describe())
    print("\n--- EDA on Cleaned Emissions Data ---")
    print(emissions_data.info())
    print(emissions_data.describe())

    # Save to SQLite database
    save_to_database(ev_data, "ev_data")
    save_to_database(emissions_data, "emissions_data")
    print("\nData pipeline executed successfully. Data saved to:", DB_PATH)

if __name__ == "__main__":
    main()
