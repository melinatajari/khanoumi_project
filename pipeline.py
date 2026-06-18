import os
import pandas as pd
from load_data import load_raw_data
from preprocess import preprocess_data
from feature_engineering import engineer_features

def run_end_to_end_pipeline():
    """Orchestrate data ingestion, preprocessing, and feature engineering."""
    print("=" * 60)
    print("INITIATING END-TO-END DATA SCIENCE PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Data Ingestion
        raw_data = load_raw_data()
        if raw_data is None or raw_data.empty:
            print("[ERROR] Pipeline aborted: Failed to load raw data.")
            return
            
        # Step 2: Data Preprocessing & Cleaning
        cleaned_data = preprocess_data(raw_data)
        if cleaned_data is None:
            print("[ERROR] Pipeline aborted: Preprocessing failed.")
            return
            
        # Step 3: Feature Engineering
        final_dataset = engineer_features(cleaned_data)
        if final_dataset is None:
            print("[ERROR] Pipeline aborted: Feature engineering failed.")
            return
            
        # Step 4: Save fully processed dataset for ML tasks
        output_filename = "processed_products.csv"
        final_dataset.to_csv(output_filename, index=False, encoding='utf-8-sig')
        
        print("=" * 60)
        print("PIPELINE EXECUTION SUCCESSFUL!")
        print(f"-> Final dataset saved to: {os.path.abspath(output_filename)}")
        print(f"-> Total shapes recorded: {final_dataset.shape}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[FATAL ERROR] Pipeline failed during execution: {e}")

if __name__ == "__main__":
    run_end_to_end_pipeline()