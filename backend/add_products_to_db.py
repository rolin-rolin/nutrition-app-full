#!/usr/bin/env python3

import sys
from pathlib import Path
import re
from app.db.session import SessionLocal
from app.db.models import Product

# Field order as per JSON schema
FIELD_ORDER = [
    "name", "brand", "description", "serving_size", "calories", "protein", "carbs", "fat", "fiber", "sugar", "electrolytes_mg", "flavor", "texture", "form", "price_usd", "categories", "dietary_flags", "timing_suitability", "tags", "allergens", "diet", "link", "image_url", "source", "verified"
]

LIST_FIELDS = {"categories", "dietary_flags", "timing_suitability", "tags", "allergens", "diet"}
FLOAT_FIELDS = {"calories", "protein", "carbs", "fat", "fiber", "sugar", "electrolytes_mg", "price_usd"}
BOOL_FIELDS = {"verified"}

def parse_product(lines):
    product = {}
    for i, field in enumerate(FIELD_ORDER):
        if i >= len(lines):
            value = "N"
        else:
            value = lines[i].strip()
        if value == "N":
            if field in FLOAT_FIELDS:
                product[field] = 0.0
            elif field in BOOL_FIELDS:
                product[field] = False
            else:
                product[field] = None
        elif field in LIST_FIELDS:
            product[field] = [v.strip() for v in value.split(",") if v.strip()] if value else []
        elif field in FLOAT_FIELDS:
            try:
                product[field] = float(value)
            except ValueError:
                product[field] = 0.0
        elif field in BOOL_FIELDS:
            product[field] = value.lower() == "t"
        else:
            product[field] = value
    return product

def main():
    if len(sys.argv) != 2:
        print("Usage: python add_products_to_db.py products_input.txt")
        sys.exit(1)
    
    input_path = sys.argv[1]
    with open(input_path, "r") as f:
        content = f.read()
    
    # Split products by "PRODUCT <number>" markers
    product_blocks = re.split(r"# PRODUCT \d+", content)
    
    # Filter out empty blocks and the first block (before any PRODUCT marker)
    raw_products = []
    for block in product_blocks[1:]:  # Skip the first block (before any PRODUCT marker)
        if block.strip():
            # Filter out comment lines (lines starting with #) and empty lines
            lines = [line.strip() for line in block.splitlines() 
                    if line.strip() and not line.strip().startswith('#')]
            if lines:  # Only add if there are non-comment, non-empty lines
                raw_products.append(lines)
    
    products = []
    for lines in raw_products:
        product = parse_product(lines)
        products.append(product)
    
    # Add products to database
    db = SessionLocal()
    try:
        added_count = 0
        for product_data in products:
            # Check if product already exists
            existing = db.query(Product).filter(Product.name == product_data['name']).first()
            if existing:
                print(f"Product '{product_data['name']}' already exists, skipping...")
                continue
            
            # Create new product
            product = Product(**product_data)
            db.add(product)
            added_count += 1
            print(f"Added: {product_data['name']}")
        
        db.commit()
        print(f"\nSuccessfully added {added_count} new products to the database.")
        
    except Exception as e:
        print(f"Error adding products: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 