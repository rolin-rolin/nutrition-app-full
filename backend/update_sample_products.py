#!/usr/bin/env python3
"""
Script to update sample products with missing fields needed for vector search.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product

def update_sample_products():
    """Update sample products with missing fields."""
    print("Updating sample products with missing fields...")
    
    db = SessionLocal()
    
    try:
        # Update each product with missing fields
        updates = [
            {
                'name': 'Protein Bar - Chocolate',
                'flavor': 'chocolate',
                'texture': 'chewy',
                'form': 'bar',
                'price_usd': 2.99,
                'tags': ['recovery', 'high-protein'],
                'allergens': ['nuts'],
                'diet': ['high-protein']
            },
            {
                'name': 'Almonds - Raw',
                'flavor': 'nutty',
                'texture': 'crunchy',
                'form': 'whole',
                'price_usd': 8.99,
                'tags': ['healthy fats', 'protein'],
                'allergens': ['tree nuts'],
                'diet': ['vegan', 'paleo']
            },
            {
                'name': 'Greek Yogurt - Vanilla',
                'flavor': 'vanilla',
                'texture': 'smooth',
                'form': 'cup',
                'price_usd': 1.49,
                'tags': ['probiotic', 'calcium'],
                'allergens': ['milk'],
                'diet': ['high-protein']
            },
            {
                'name': 'Banana',
                'flavor': 'sweet',
                'texture': 'soft',
                'form': 'whole',
                'price_usd': 0.25,
                'tags': ['potassium', 'natural'],
                'allergens': [],
                'diet': ['vegan', 'paleo']
            },
            {
                'name': 'Trail Mix - Savory',
                'flavor': 'savory',
                'texture': 'crunchy',
                'form': 'mix',
                'price_usd': 4.99,
                'tags': ['energy', 'portable'],
                'allergens': ['nuts'],
                'diet': ['vegan']
            },
            {
                'name': 'Protein Shake - Vanilla',
                'flavor': 'vanilla',
                'texture': 'smooth',
                'form': 'powder',
                'price_usd': 29.99,
                'tags': ['muscle building', 'convenient'],
                'allergens': ['milk'],
                'diet': ['high-protein']
            },
            {
                'name': 'Hummus - Classic',
                'flavor': 'savory',
                'texture': 'smooth',
                'form': 'dip',
                'price_usd': 3.99,
                'tags': ['fiber', 'plant protein'],
                'allergens': ['sesame'],
                'diet': ['vegan', 'mediterranean']
            },
            {
                'name': 'Oatmeal - Steel Cut',
                'flavor': 'neutral',
                'texture': 'chewy',
                'form': 'grain',
                'price_usd': 5.99,
                'tags': ['fiber', 'sustained energy'],
                'allergens': [],
                'diet': ['vegan', 'gluten-free']
            },
            {
                'name': 'Cottage Cheese - Low Fat',
                'flavor': 'mild',
                'texture': 'lumpy',
                'form': 'cup',
                'price_usd': 2.49,
                'tags': ['casein protein', 'calcium'],
                'allergens': ['milk'],
                'diet': ['high-protein']
            },
            {
                'name': 'Sweet Potato - Baked',
                'flavor': 'sweet',
                'texture': 'soft',
                'form': 'whole',
                'price_usd': 1.99,
                'tags': ['complex carbs', 'vitamin A'],
                'allergens': [],
                'diet': ['vegan', 'paleo']
            }
        ]
        
        for update_data in updates:
            product = db.query(Product).filter(Product.name == update_data['name']).first()
            if product:
                product.flavor = update_data['flavor']
                product.texture = update_data['texture']
                product.form = update_data['form']
                product.price_usd = update_data['price_usd']
                product.tags = update_data['tags']
                product.allergens = update_data['allergens']
                product.diet = update_data['diet']
                print(f"Updated: {product.name}")
        
        db.commit()
        print("Successfully updated all sample products!")
        
    except Exception as e:
        print(f"Error updating products: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_sample_products() 