import os
import json
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database Connection Setup
engine = create_engine("sqlite:///khanoumi.db", echo=False)
Base = declarative_base()

# 2. Database Schema Design
class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    main_category = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    scraped_id = Column(String)  
    name = Column(String)
    brand = Column(String)
    price = Column(Integer)
    rate = Column(Float, default=0.0)
    rates_count = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    comment_uuid = Column(String)  
    product_id = Column(Integer, ForeignKey('products.product_id'))
    user_name = Column(String)
    description = Column(Text)
    like_count = Column(Integer, default=0)
    is_buyer = Column(Boolean, default=False)
    created_at = Column(String)

# Recreate database tables from scratch
print("Dropping and recreating database tables...")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Define base path for raw scraped JSON data
base_path = Path(r"D:\EE-Term8\Data Sciences\Final Project\scraped_data")

print("Starting data import from JSON files...")
inserted_products = 0
inserted_reviews = 0

for detail_file in base_path.rglob("detail.json"):
    try:
        sub_cat_name = detail_file.parents[2].name
        main_cat_name = detail_file.parents[3].name

        # 3. Check or Create Category
        category = session.query(Category).filter_by(
            main_category=main_cat_name,
            sub_category=sub_cat_name
        ).first()

        if not category:
            category = Category(main_category=main_cat_name, sub_category=sub_cat_name)
            session.add(category)
            session.commit()  

        # 4. Parse Product Details
        with open(detail_file, 'r', encoding='utf-8') as f:
            product_data = json.load(f)

        p_scraped_id = str(product_data.get('id', ''))
        p_name = product_data.get('nameFa') or product_data.get('pageH1') or "Unknown"
        
        brand_obj = product_data.get('brand')
        p_brand = brand_obj.get('nameFa') if brand_obj else "Unknown"
        if not p_brand:
            p_brand = "Unknown"

        p_price = product_data.get('basePrice') or 0
        p_rate = float(product_data.get('rate') or 0.0)
        p_rates_count = int(product_data.get('ratesCount') or 0)

        product = Product(
            scraped_id=p_scraped_id,
            name=str(p_name).strip(),
            brand=str(p_brand).strip(),
            price=p_price,
            rate=p_rate,
            rates_count=p_rates_count,
            category_id=category.category_id
        )
        
        session.add(product)
        session.flush()  
        inserted_products += 1

        # 5. Parse Product Reviews
        comments_file = detail_file.parent / "comments.json"
        if comments_file.exists():
            with open(comments_file, 'r', encoding='utf-8') as f:
                comments_data = json.load(f)
            
            comment_items = comments_data.get('items', [])
            reviews_to_add = []
            
            for item in comment_items:
                u_name = item.get('userName') or "Unknown"
                desc = item.get('description') or ""
                likes = item.get('likeCount') or 0
                buyer_status = bool(item.get('isBuyer', False))
                date_str = item.get('createdAt') or ""
                c_uuid = item.get('id') or ""

                review = Review(
                    comment_uuid=c_uuid,
                    product_id=product.product_id,
                    user_name=str(u_name).strip(),
                    description=str(desc).strip(),
                    like_count=likes,
                    is_buyer=buyer_status,
                    created_at=date_str
                )
                reviews_to_add.append(review)
                inserted_reviews += 1
            
            if reviews_to_add:
                session.add_all(reviews_to_add)

        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error processing file {detail_file}: {e}")

print("=" * 60)
print("DATA MIGRATION SUCCESSFUL!")
print(f"Total Products Imported: {inserted_products}")
print(f"Total Reviews Imported: {inserted_reviews}")
print("=" * 60)

session.close()