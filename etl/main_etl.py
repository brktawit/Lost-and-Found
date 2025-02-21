import os
import pandas as pd
from etl.extract.fetch_kaggle_data import download_kaggle_dataset, load_dataset
from etl.transform.drop_unnecessary_fields import drop_unnecessary_fields
from etl.transform.assign_categories import assign_categories
from etl.transform.add_coordinates import add_coordinates


def run_etl():
    """
    Executes the ETL (Extract, Transform, Load) process for the Delhi Metro lost and found dataset.

    The function performs the following steps:
    1. Checks if the dataset is already downloaded; if not, it downloads it from Kaggle.
    2. Loads the dataset into a pandas DataFrame.
    3. Limits the dataset to the first 1,000 rows for processing.
    4. Applies transformations to the dataset, including:
       - Dropping unnecessary fields
       - Assigning categories to items
       - Adding geographic coordinates based on station names.
    5. Saves the transformed dataset to a CSV file for further validation and use.

    """
    
    # Define expected dataset path
    dataset_path = "etl/data/raw/delhimetrorail.csv"

    # Check if dataset already exists to avoid re-downloading
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

    # Step 3: Transform the data
    df = drop_unnecessary_fields(df) # Remove unnecessary columns
    df = assign_categories(df)  # Assign categories based on item names
    df = add_coordinates(df)  # Add coordinates based on station names

    # Step 4: Save Transformed Data for Validation
    transformed_path = "etl/data/processed/transformed_data_with_coordinates.csv"
    df.to_csv(transformed_path, index=False)

    print(f"✅ Transformed dataset with coordinates saved at {transformed_path}")
    print(df.head())  # Display the first 5 rows for verification

if __name__ == "__main__":
    run_etl()
