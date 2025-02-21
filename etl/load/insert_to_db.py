import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String, Text, Date, Float
from geoalchemy2 import Geometry
import os

# Database Configuration
DB_URL = "postgresql://postgres:postgres@localhost/Trial"
engine = create_engine(DB_URL)

# Path to Processed CSV File
csv_file = os.path.join(os.path.dirname(__file__), "../data/processed/transformed_data_with_coordinates.csv")

# Load CSV into DataFrame
df = pd.read_csv(csv_file)

# Assign `user_id = 2` to make sure all the datas from kaggle are assigned to admin in the source column
df["user_id"] = 2  

# Add source column with 'admin' for Kaggle data
#df["source"] = "admin"

# Ensure 'user_id' is filled correctly
#df["user_id"] = df["user_id"].fillna(2)  # Default user_id to 2 for Kaggle/admin data

# Convert `receiving_date` to the correct format for PostgreSQL
df["receiving_date"] = pd.to_datetime(df["receiving_date"], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")

# Map `category_name` to `category_id` (from database)
category_mapping = {
    "Electronics": 15,
    "Bags": 16,
    "Clothing": 17,
    "Documents": 18,
    "Household Items": 19,
    "Personal Accessories": 20,
    "Miscellaneous": 21
}

df["category_id"] = df["category_name"].map(category_mapping)

# Ensure missing values (`category_id`, `item_name`, `station_name`, `longitude`, `latitude`) are set to NULL
df["category_id"] = df["category_id"].astype("Int64")  # Use Int64 to allow NULL values
df["item_name"] = df["item_name"].replace("", None)  # Replace empty strings with NULL
df["station_name"] = df["station_name"].replace("", None)  # Replace empty strings with NULL
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")  # Convert to float, keep NaNs
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")  # Convert to float, keep NaNs


# Convert `latitude` & `longitude` into PostGIS `GEOMETRY(Point, 4326)`
df["location"] = df.apply(
    lambda row: f"SRID=4326;POINT({row['longitude']} {row['latitude']})" if pd.notnull(row["longitude"]) and pd.notnull(row["latitude"]) else None, axis=1
)

# Rename `station_name` to `place`
df.rename(columns={"station_name": "place"}, inplace=True)

# Drop `latitude` and `longitude` since they're now stored in `location`
df.drop(columns=["latitude", "longitude"], inplace=True)

# Insert Data into PostgreSQL (without `item_id`, as it's auto-incremented)
df.to_sql("lostitems", engine, if_exists="append", index=False, method='multi',
          dtype={
              "item_name": String(100),
              "description": Text,
              "receiving_date": Date,
              "category_name": Text,
              "category_id": Integer,
              "user_id": Integer,
              "place": String(100),
              "location": Geometry("POINT", srid=4326)
          })

print("✅ CSV data loaded successfully into PostgreSQL!")
