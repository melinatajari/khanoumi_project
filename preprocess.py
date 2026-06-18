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
    from load_data import load_raw_data
    raw_df = load_raw_data()
    if raw_df is not None:
        clean_df = preprocess_data(raw_df)