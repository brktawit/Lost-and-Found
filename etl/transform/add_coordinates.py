#For applying coordinates to the dataset

import pandas as pd
from etl.transform.station_coordinates import station_coordinates

def add_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds latitude and longitude to the dataset based on station names.

    Args:
        df (pd.DataFrame): Input DataFrame with a 'station_name' column.

    Returns:
        pd.DataFrame: Transformed DataFrame with 'latitude' and 'longitude' columns.
    """
    # Map station names to latitude and longitude
    df['latitude'] = df['station_name'].map(lambda x: station_coordinates.get(x, (None, None))[0])
    df['longitude'] = df['station_name'].map(lambda x: station_coordinates.get(x, (None, None))[1])

    # Identify and log missing coordinates
    missing_stations = df[df['latitude'].isnull() | df['longitude'].isnull()]['station_name'].unique()
    if len(missing_stations) > 0:
        print(f"Stations missing coordinates: {missing_stations}")
        # Optional: Save missing stations to a file for future updates
        pd.DataFrame(missing_stations, columns=['station_name']).to_csv('etl/data/missing_stations.csv', index=False)

    return df
