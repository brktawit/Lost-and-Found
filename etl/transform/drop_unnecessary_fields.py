import pandas as pd

def drop_unnecessary_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes unnecessary columns from the dataset.
    
    Note:
        This function checks for the existence of specified columns before attempting to drop them.
        It avoids raising an error if any of the specified columns are not present in the DataFrame.
    """
    # List of columns that are unnecessary and will be removed
    columns_to_remove = ['item_quantity', 'receiving_time']
    
    # Drop the specified columns from the DataFrame if they exist
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
    
    print("🗑️ Removed unnecessary columns.")
    return df
