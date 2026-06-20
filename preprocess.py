import pandas as pd
import numpy as np

def preprocess_data(df):
    """Clean raw dataframe and handle missing values."""
    if df is None or df.empty:
        print("Empty dataframe received.")
        return None
        
    print("Preprocessing data...")
    df_clean = df.copy()
    
    # 1. Handle zero prices using sub-category median
    df_clean['price'] = df_clean['price'].replace(0, np.nan)
    df_clean['price'] = df_clean.groupby('sub_category')['price'].transform(lambda x: x.fillna(x.median()))
    df_clean['price'] = df_clean['price'].fillna(df_clean['price'].median()).astype(int)
    
    # 2. Handle missing or generic brands
    df_clean['brand'] = df_clean['brand'].fillna('Unknown')
    df_clean['brand'] = df_clean['brand'].replace(['متفرقه', '', 'nan'], 'Unknown')
    
    # 3. Handle missing rating values safely
    df_clean['rate'] = df_clean['rate'].fillna(0.0).astype(float)
    df_clean['rates_count'] = df_clean['rates_count'].fillna(0).astype(int)
    
    print(f"Preprocessing finished. Data shape: {df_clean.shape}")
    return df_clean

if __name__ == "__main__":
    import sys
    import os
    import pandas as pd

    input_path = os.path.abspath("raw_data.csv")
    output_path = os.path.abspath("cleaned_data.csv")

    # Process Helpers: Ingestion :
    if not os.path.exists(input_path):
        print(f"Fatal error: Input payload not found at {input_path}")
        sys.exit(1)

    try:
        raw_df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Fatal error: Failed to parse input payload: {e}")
        sys.exit(1)

    # Process Helpers: Transformation :
    clean_df = preprocess_data(raw_df)

    # Process Helpers: Serialization :
    if clean_df is not None and not clean_df.empty:
        clean_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Preprocessing successful. Payload serialized to {output_path}")
        sys.exit(0)

    print("Preprocessing failed to generate valid payload. Aborting pipeline.")
    sys.exit(1)