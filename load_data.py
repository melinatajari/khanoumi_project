# load_data.py
import pandas as pd
from database_connection import get_database_connection

def load_raw_data():
    """Connect to database and fetch products joined with category and aggregated review metrics."""
    print("Loading raw data from database...")
    conn = get_database_connection()
    
    if conn is None:
        raise Exception("Database connection failed. Cannot load data.")
    
    # Enhanced query to extract statistics from both products and reviews tables
    query = """
    SELECT 
        p.product_id, 
        p.name, 
        p.brand, 
        p.price, 
        p.rate, 
        p.rates_count, 
        c.main_category, 
        c.sub_category,
        COUNT(r.review_id) AS review_count,
        AVG(r.like_count) AS avg_comment_likes,
        AVG(LENGTH(r.description)) AS comment_length_avg
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN reviews r ON p.product_id = r.product_id
    GROUP BY p.product_id;
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        print(f"Data loaded successfully. Total records retrieved: {len(df)}")
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    import os

    # Process Helpers: Extraction :
    df = load_raw_data()

    # Process Helpers: Serialization :
    if df is not None and not df.empty:
        output_path = os.path.abspath("raw_data.csv")
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Extraction successful. Payload serialized to {output_path}")
        sys.exit(0)
    
    print("Extraction failed or dataset is empty. Aborting pipeline.")
    sys.exit(1)