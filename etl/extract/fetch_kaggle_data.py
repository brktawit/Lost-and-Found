import os
import zipfile
import shutil
import pandas as pd

def download_kaggle_dataset():
    """
    Downloads the dataset using Kaggle API and moves it to the ETL data folder.

    :return: Path to the downloaded dataset file, or None if the download failed.
    """
    print("⏳ Downloading dataset from Kaggle...")

    # Specify the dataset and download the ZIP file using Kaggle API
    os.system("kaggle datasets download -d forgetabhi/delhi-metro-lost-and-found-dataset")

    # Define the path for the downloaded ZIP file
    zip_file_path = "delhi-metro-lost-and-found-dataset.zip"
    etl_raw_folder = "etl/data/raw"
    os.makedirs(etl_raw_folder, exist_ok=True)

    # Check if the ZIP file exists and extract it
    if os.path.exists(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(etl_raw_folder)
        print(f"✅ Dataset extracted to {etl_raw_folder}")
    else:
        print("❌ Dataset ZIP file not found. Please check the download process.")
        return None

    print("Files in the raw data folder:", os.listdir(etl_raw_folder))

    # Return the path of the first CSV file found
    downloaded_files = os.listdir(etl_raw_folder)
    if not downloaded_files:
        print("❌ No files found in the raw data folder. Please check the download process.")
        return None
    return os.path.join(etl_raw_folder, downloaded_files[0])

if __name__ == "__main__":
    dataset_path = download_kaggle_dataset()
    if dataset_path:
        df = pd.read_csv(dataset_path)
        print(df.head())
    else:
        print("❌ Dataset path is None. Exiting.")