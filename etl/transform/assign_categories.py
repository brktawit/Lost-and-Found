import pandas as pd

# Predefined category mapping
category_mapping = {
    "Electronics": ["mobile", "earbud", "laptop", "charger", "tablet", "camera", "headphone", "power bank", "earphone", "stethoscope", "i pad", "tripod", "standee", "led clock"],
    "Bags": ["bag", "backpack", "suitcase", "briefcase"],
    "Clothing": ["jacket", "shirt", "trouser", "jeans", "scarf", "sweater", "cap", "shoes", "glove", "blanket", "coat cover", "blazer", "cushion cover", "coat", "clothes", "slipper", "cloth", "bedsheet", "lady suits", "shoe"],
    "Documents": ["card", "passport", "license", "driving license", "debit card", "credit card", "id", "file", "books", "medical report"],
    "Household Items": ["utensils", "hanger", "lunch box", "bottle", "towel", "key", "torch", "helmet"],
    "Personal Accessories": ["purse", "wallet", "watch", "chain", "glasses", "ring", "bangle", "umbrella", "bracelet", "anklet"],
    "Miscellaneous": []  # Default category for uncategorized items
}


def assign_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns categories based on item names.
    If an item is not found in the mapping, it is categorized as 'Miscellaneous'.
    - Converts item names to lowercase.
    - Strips leading/trailing spaces.
    - Ensures matching is not case or space sensitive.
    """
    def categorize_item(item_name):
        for category, keywords in category_mapping.items():
            for keyword in keywords:
                if keyword in item_name:  # Check if keyword is in item_name
                    return category
        return "Miscellaneous"  # Default category if no match

    # Normalize item names and assign categories
    df['normalized_item_name'] = df['item_name'].str.lower().str.strip()
    df['category_name'] = df['normalized_item_name'].apply(categorize_item)

    print("✅ Assigned categories based on item names.")
    return df.drop(columns=['normalized_item_name'])  # Remove the helper column