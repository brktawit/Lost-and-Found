import kagglehub  # Ensure KaggleHub is installed: pip install kagglehub
import shutil
import os
import pandas as pd

def download_kaggle_dataset():
    """
    Downloads the dataset using KaggleHub and moves it to the ETL data folder.
    
    :param dataset_url: URL of the dataset to download
    :param etl_raw_folder: Path to the ETL raw data folder
    """
    print("⏳ Downloading dataset from Kaggle...")
    dataset_folder = kagglehub.dataset_download("forgetabhi/delhi-metro-lost-and-found-dataset")

    # Define where to move the dataset within the ETL pipeline
    etl_raw_folder = "etl/data/raw"
    os.makedirs(etl_raw_folder, exist_ok=True)  # Ensure the folder exists

    # Move the dataset files to the ETL raw folder
    for file in os.listdir(dataset_folder):
        source_path = os.path.join(dataset_folder, file)
        dest_path = os.path.join(etl_raw_folder, file)
        shutil.move(source_path, dest_path)

    print(f"✅ Dataset downloaded and moved to {etl_raw_folder}")

    # Return the path of the downloaded dataset (for future loading)
    return os.path.join(etl_raw_folder, os.listdir(etl_raw_folder)[0])


if __name__ == "__main__":
    dataset_path = download_kaggle_dataset()
    df = pd.read_csv(dataset_path)
    print (df.head())
