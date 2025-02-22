import os
import pandas as pd
from etl.extract.fetch_kaggle_data import download_kaggle_dataset
from etl.transform.drop_unnecessary_fields import drop_unnecessary_fields
from etl.transform.assign_categories import assign_categories
from etl.transform.add_coordinates import add_coordinates
from etl.load.insert_to_db import load_to_database  # Import the function to load data to the database


def load_dataset(dataset_path: str) -> pd.DataFrame:
    """
    Loads the dataset into a pandas DataFrame.
    
    Args:
        dataset_path (str): Path to the dataset CSV file.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return pd.read_csv(dataset_path)

def run_etl():
    """
    Executes the ETL (Extract, Transform, Load) process for the dataset.
    """
    # Define expected dataset path
    raw_data_folder = os.path.join("etl", "data", "raw")
    dataset_path = os.path.join(raw_data_folder, "delhimetrorail.csv")
    os.makedirs(raw_data_folder, exist_ok=True)
    
    # Step 1: Download dataset if not present
    if not os.path.exists(dataset_path):
        print("⏳ Dataset not found. Downloading from Kaggle...")
        dataset_path = download_kaggle_dataset()
    else:
        print(f"✅ Dataset already exists at {dataset_path}. Skipping download.")
    
    # Step 2: Load the dataset
    df = load_dataset(dataset_path)
    
    # Step 3: Limit dataset to first 1,000 rows
    df = df.head(1000)
    print(f"📊 Dataset limited to {len(df)} rows.")
    
    # Step 4: Apply Transformations
    df = drop_unnecessary_fields(df) # Remove unnecessary columns
    df = assign_categories(df)  # Assign categories based on item names
    df = add_coordinates(df)  # Add coordinates based on station names
    
    # Step 5: Save Transformed Data
    processed_data_folder = os.path.join("etl", "data", "processed")
    os.makedirs(processed_data_folder, exist_ok=True)
    transformed_path = os.path.join(processed_data_folder, "transformed_data_with_coordinates.csv")
    df.to_csv(transformed_path, index=False)
    
    print(f"✅ Transformed dataset saved at {transformed_path}")
    print(df.head())
    
    # Step 6: Load transformed data into the database
    load_to_database(transformed_path)  # Call the function to insert data into the database

if __name__ == "__main__":
    run_etl()