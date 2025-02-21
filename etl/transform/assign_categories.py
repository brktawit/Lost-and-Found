import pandas as pd

# Predefined category mapping for item names to their corresponding categories
category_mapping = {
    "Electronics": ["mobile", "earbud", "laptop", "charger", "tablet", "camera", "headphone", "power bank", "earphone", "stethoscope", "i pad", "tripod", "standee", "led clock"],
    "Bags": ["bag", "backpack", "suitcase", "briefcase"],
    "Clothing": ["jacket", "shirt", "trouser", "jeans", "scarf", "sweater", "cap", "shoes", "glove", "blanket", "coat cover", "blazer", "cushion cover", "coat", "clothes", "slipper", "cloth", "bedsheet", "lady suits", "shoe"],
    "Documents": ["card", "passport", "license", "driving license", "debit card", "credit card", "id", "file", "books", "medical report"],
    "Household Items": ["utensils", "hanger", "lunch box", "bottle", "towel", "key", "torch", "helmet"],
    "Personal Accessories": ["purse", "wallet", "watch", "chain", "glasses", "ring", "bangle", "umbrella", "bracelet", "anklet"],
    "Miscellaneous": []  # Default category for items that do not match any keyword
}


def assign_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns categories to items based on their names.

    Args:
        df (pd.DataFrame): Input DataFrame with an 'item_name' column.

    Returns:
        pd.DataFrame: Updated DataFrame with an additional 'category_name' column based on item names.
    
    Note:
        - Each item name is converted to lowercase and stripped of leading/trailing spaces
          to ensure matching is case and space insensitive.
        - If an item name does not match any predefined keywords, it is categorized as 'Miscellaneous'.
    
    """
    
    def categorize_item(item_name):
        """
        Determines the category for a given item name based on predefined keywords.

        Args:
            item_name (str): The name of the item to categorize.

        Returns:
            str: The category name assigned to the item.
        """
        
        for category, keywords in category_mapping.items():
            for keyword in keywords:
                if keyword in item_name:  # Check if the keyword is present in the item name
                    return category
        return "Miscellaneous"  # Default category if no match
    

    # Normalize item names and assign categories
    df['normalized_item_name'] = df['item_name'].str.lower().str.strip()
    df['category_name'] = df['normalized_item_name'].apply(categorize_item)

    print("✅ Assigned categories based on item names.")
    return df.drop(columns=['normalized_item_name'])  # Remove the helper column