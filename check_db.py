# check_db.py
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import arabic_reshaper
from bidi.algorithm import get_display

def fix_persian_text(text):
    """Fix Persian text alignment for terminal display."""
    if not text:
        return "No Text"
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

def check_database():
    print("Connecting to the database to verify data...")
    
    base_dir = Path(__file__).resolve().parent
    db_path = base_dir / "khanoumi.db"
    
    engine = create_engine(f"sqlite:///{db_path}")

    try:
        total_reviews = pd.read_sql("SELECT COUNT(*) FROM reviews;", engine).iloc[0, 0]
        total_products = pd.read_sql("SELECT COUNT(*) FROM products;", engine).iloc[0, 0]
        
        print(f"[SUCCESS] Verified: Found {total_products} products and {total_reviews} reviews.")
        print("-" * 60)

        # SQL Query to get top 5 products based on rating and review likes
        query = """
        SELECT r.user_name, r.like_count, p.name AS product_name, p.rate AS product_rating, r.description 
        FROM reviews r
        JOIN products p ON r.product_id = p.product_id
        WHERE p.rate > 0 
        ORDER BY p.rate DESC, r.like_count DESC
        LIMIT 5;
        """
        
        sample_df = pd.read_sql(query, engine)
        
        print("Sample of 5 reviews successfully extracted from the database:\n")
        for index, row in sample_df.iterrows():
            # Apply Persian text fix before printing
            user = fix_persian_text(row['user_name'])
            product = fix_persian_text(row['product_name'])
            
            comment_snippet = str(row['description'])[:100] if row['description'] else "No review text available"
            comment = fix_persian_text(comment_snippet)
            
            print(f"👤 User: {user} (Likes: {row['like_count']})")
            print(f"🛍️ Product: {product}")
            print(f"⭐ Product Rating: {row['product_rating']} out of 5.0")
            print(f"💬 Comment: {comment}...") 
            print("-" * 40)
            
    except Exception as e:
        print(f"[ERROR] An error occurred while querying the database: {e}")

if __name__ == "__main__":
    check_database()