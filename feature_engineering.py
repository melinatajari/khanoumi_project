# feature_engineering.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess import preprocess_data
from load_data import load_raw_data

def engineer_features(df):
    """Extract advanced product and user feedback features from dataframe."""
    if df is None or df.empty:
        print("Empty dataframe received.")
        return None
        
    df_features = df.copy()
    print("Starting advanced feature engineering...")
    
    # --- SECTION 1: Product-Specific Features ---
    top_brands_list = ['بیوآکوا', 'ورژن', 'اوریف‌لیم', 'کامان', 'سینره', 'لافارر']
    df_features['is_top_brand'] = df_features['brand'].apply(lambda x: 1 if x in top_brands_list else 0)
    df_features['name_length'] = df_features['name'].apply(lambda x: len(str(x)) if pd.notnull(x) else 0)
    df_features['main_category_encoded'] = df_features['main_category'].map({'makeup': 1, 'skincare': 0}).fillna(-1)
    
    # Safe price segmentation (0: Cheap, 1: Medium, 2: Expensive) within each sub-category
    def segment_price(group):
        if group.nunique() < 3:
            return pd.Series(1, index=group.index)
        try:
            return pd.qcut(group, q=3, labels=[0, 1, 2], duplicates='drop')
        except ValueError:
            return pd.Series(1, index=group.index)
        
    df_features['price_segment'] = df_features.groupby('sub_category')['price'].transform(segment_price).astype(int)

    # --- SECTION 2: User Feedback Features (Database Aggregrations) ---
    df_features['review_count'] = df_features['review_count'].fillna(0).astype(int)
    df_features['avg_comment_likes'] = df_features['avg_comment_likes'].fillna(0.0).astype(float)
    df_features['comment_length_avg'] = df_features['comment_length_avg'].fillna(0.0).astype(float)

    # --- SECTION 3: Advanced Interaction Terms ---
    df_features['popularity_score'] = df_features['rate'] * np.log1p(df_features['rates_count'])
    
    # Normalization / Scaling
    scaler = MinMaxScaler()
    df_features[['price_scaled', 'name_length_scaled', 'rate_scaled']] = scaler.fit_transform(
        df_features[['price', 'name_length', 'rate']]
    )
    
    df_features['value_for_money_index'] = df_features['rate'] / (df_features['price_scaled'] + 0.01)

    # --- SECTION 4: Categorical Variables Encoding ---
    brand_freq = df_features['brand'].value_counts(normalize=True)
    subcat_freq = df_features['sub_category'].value_counts(normalize=True)
    df_features['brand_encoded'] = df_features['brand'].map(brand_freq)
    df_features['sub_category_encoded'] = df_features['sub_category'].map(subcat_freq)

    # --- SECTION 5: Text Vectorization ---
    tfidf = TfidfVectorizer(max_features=10)
    tfidf_matrix = tfidf.fit_transform(df_features['name'].fillna(''))
    tfidf_cols = [f"tfidf_{word}" for word in tfidf.get_feature_names_out()]
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_cols, index=df_features.index)
    
    df_features = pd.concat([df_features, tfidf_df], axis=1)
    
    print(f"Advanced feature engineering completed. Data shape: {df_features.shape}")
    return df_features

if __name__ == "__main__":
    raw_df = load_raw_data()
    if raw_df is not None:
        cleaned_df = preprocess_data(raw_df)
        if cleaned_df is not None:
            final_featured_df = engineer_features(cleaned_df)
            
            # Save the processed data as a CSV file to satisfy the last requirement
            if final_featured_df is not None:
                output_file = "final_processed_data.csv"
                final_featured_df.to_csv(output_file, index=False, encoding='utf-8-sig')
                print(f"Processed dataset successfully saved to: {output_file}")