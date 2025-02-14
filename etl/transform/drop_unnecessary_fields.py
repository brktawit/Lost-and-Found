import pandas as pd

def drop_unnecessary_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes unnecessary columns from the dataset.
    """
    columns_to_remove = ['item_quantity', 'receiving_time']
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
    print("🗑️ Removed unnecessary columns.")
    return df
