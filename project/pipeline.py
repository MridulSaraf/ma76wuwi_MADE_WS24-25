import os
import pandas as pd
import sqlite3

# Set paths
DATA_DIR = "/data"
DB_PATH = os.path.join(DATA_DIR, "project_data.db")


ev_data_url = "https://github.com/MridulSaraf/Data4MADE/blob/main/IEA-EV-dataEV%20salesHistoricalCars.csv" 
emissions_data_url = "https://github.com/MridulSaraf/Data4MADE/blob/main/b61929c4-3c0f-4ab6-ae58-6ab62624d304_Data.csv" 

# Create /data directory if it doesn’t exist
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
    # Example transformations: rename columns, handle missing values
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    # Filter relevant columns if necessary, e.g., country, year, EV_sales
    df.fillna(method='ffill', inplace=True)
    return df

def clean_transform_emissions_data(df):
    """Cleans and transforms emissions data."""
    # Example transformations: rename columns, handle missing values
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    # Filter relevant columns if necessary, e.g., country, year, CO2_emissions
    df.fillna(method='ffill', inplace=True)
    return df

def save_to_database(df, table_name):
    """Saves DataFrame to SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

def main():
    # Step 1: Load datasets from local paths
    ev_data = load_data(ev_data_url)
    emissions_data = load_data(emissions_data_url)
    
    # Step 2: Clean and transform datasets
    ev_data = clean_transform_ev_data(ev_data)
    emissions_data = clean_transform_emissions_data(emissions_data)
    
    # Step 3: Save to SQLite database
    save_to_database(ev_data, "ev_data")
    save_to_database(emissions_data, "emissions_data")
    print("Data pipeline executed successfully. Data saved to:", DB_PATH)

if __name__ == "__main__":
    main()
