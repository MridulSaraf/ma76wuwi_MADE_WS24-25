import os
import pandas as pd
import sqlite3


DATA_DIR = "/data"
DB_PATH = os.path.join(DATA_DIR, "project_data.db")


ev_data_url = "https://github.com/MridulSaraf/Data4MADE/blob/main/IEA-EV-dataEV%20salesHistoricalCars.csv" 
emissions_data_url = "https://github.com/MridulSaraf/Data4MADE/blob/main/b61929c4-3c0f-4ab6-ae58-6ab62624d304_Data.csv" 

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

def eda(df, dataset_name):
    """Performing EDA on the dataset."""
    print(f"\nExploratory Data Analysis: {dataset_name}")
    
    # Basic Info
    print("\n--- Basic Information ---")
    print(df.info())
    
    # Summary Statistics
    print("\n--- Summary Statistics ---")
    print(df.describe())
    
    # Check for Missing Values
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    
    # Check for Duplicates
    duplicates = df.duplicated().sum()
    print(f"\n--- Duplicate Rows ---\n{duplicates} duplicate rows found.")
    
    # Unique Values in Columns
    print("\n--- Unique Values Per Column ---")
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"{col}: {unique_count} unique values")
    
    # Value Counts for Categorical Columns
    print("\n--- Value Counts for Categorical Columns ---")
    for col in df.select_dtypes(include=['object']).columns:
        print(f"\n{col}:")
        print(df[col].value_counts().head())

def main():
    # Load datasets
    ev_data = load_data(ev_data_url)
    emissions_data = load_data(emissions_data_url)
    
    # EDA on raw data
    eda(ev_data, "EV Data (Raw)")
    eda(emissions_data, "Emissions Data (Raw)")
    
    # Clean and transform datasets
    ev_data = clean_transform_ev_data(ev_data)
    emissions_data = clean_transform_emissions_data(emissions_data)
    
    # EDA on cleaned data
    eda(ev_data, "EV Data (Cleaned)")
    eda(emissions_data, "Emissions Data (Cleaned)")
    
    # Save to SQLite database
    save_to_database(ev_data, "ev_data")
    save_to_database(emissions_data, "emissions_data")
    print("\nData pipeline executed successfully. Data saved to:", DB_PATH)

if __name__ == "__main__":
    main()
    
