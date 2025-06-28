#!/usr/bin/env python3
"""
Database initialization script.
Creates tables and adds sample product data for testing.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.db.session import engine, SessionLocal
from app.db.models import Base, Product, UserInput, MacroTarget, RecommendationResponse

def init_db():
    """Initialize the database with tables and sample data."""
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if we already have products
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print(f"Database already has {existing_products} products. Skipping sample data creation.")
            return
        
        # Add sample products
        print("Adding sample products...")
        sample_products = [
            Product(
                name="Protein Bar - Chocolate",
                brand="PowerFuel",
                description="High protein chocolate bar with 20g protein, good for post-workout recovery",
                serving_size="1 bar (60g)",
                calories=220,
                protein=20.0,
                carbs=15.0,
                fat=8.0,
                fiber=3.0,
                sugar=5.0,
                categories=["protein bar", "chocolate", "sweet"],
                dietary_flags=["high-protein"],
                timing_suitability=["post-workout"],
                source="sample_data"
            ),
            Product(
                name="Almonds - Raw",
                brand="Nature's Best",
                description="Raw almonds, great source of healthy fats and protein",
                serving_size="1/4 cup (28g)",
                calories=160,
                protein=6.0,
                carbs=6.0,
                fat=14.0,
                fiber=3.0,
                sugar=1.0,
                categories=["nuts", "savory", "crunchy"],
                dietary_flags=["vegan", "gluten-free"],
                timing_suitability=["post-workout", "general"],
                source="sample_data"
            ),
            Product(
                name="Greek Yogurt - Vanilla",
                brand="CreamyGood",
                description="High protein vanilla Greek yogurt, smooth and creamy",
                serving_size="1 cup (170g)",
                calories=130,
                protein=15.0,
                carbs=8.0,
                fat=2.0,
                fiber=0.0,
                sugar=6.0,
                categories=["dairy", "yogurt", "sweet"],
                dietary_flags=["high-protein", "gluten-free"],
                timing_suitability=["post-workout", "general"],
                source="sample_data"
            ),
            Product(
                name="Banana",
                brand="FreshFruit",
                description="Natural banana, excellent source of potassium and carbs",
                serving_size="1 medium (118g)",
                calories=105,
                protein=1.3,
                carbs=27.0,
                fat=0.4,
                fiber=3.1,
                sugar=14.0,
                categories=["fruit", "sweet"],
                dietary_flags=["vegan", "gluten-free"],
                timing_suitability=["post-workout", "pre-workout"],
                source="sample_data"
            ),
            Product(
                name="Trail Mix - Savory",
                brand="TrailBlazer",
                description="Savory trail mix with nuts, seeds, and dried vegetables",
                serving_size="1/4 cup (30g)",
                calories=150,
                protein=5.0,
                carbs=8.0,
                fat=12.0,
                fiber=3.0,
                sugar=2.0,
                categories=["trail mix", "savory", "crunchy"],
                dietary_flags=["vegan", "gluten-free"],
                timing_suitability=["post-workout", "general"],
                source="sample_data"
            ),
            Product(
                name="Protein Shake - Vanilla",
                brand="MuscleFuel",
                description="Vanilla protein shake with 25g protein, smooth and creamy",
                serving_size="1 scoop (30g)",
                calories=120,
                protein=25.0,
                carbs=3.0,
                fat=1.0,
                fiber=0.0,
                sugar=1.0,
                categories=["protein shake", "sweet"],
                dietary_flags=["high-protein", "gluten-free"],
                timing_suitability=["post-workout"],
                source="sample_data"
            ),
            Product(
                name="Hummus - Classic",
                brand="Mediterranean",
                description="Classic hummus made with chickpeas, tahini, and olive oil",
                serving_size="2 tbsp (30g)",
                calories=80,
                protein=2.0,
                carbs=6.0,
                fat=5.0,
                fiber=2.0,
                sugar=0.0,
                categories=["dip", "savory"],
                dietary_flags=["vegan", "gluten-free"],
                timing_suitability=["general"],
                source="sample_data"
            ),
            Product(
                name="Oatmeal - Steel Cut",
                brand="HeartHealthy",
                description="Steel cut oatmeal, high in fiber and complex carbs",
                serving_size="1/2 cup cooked (80g)",
                calories=150,
                protein=5.0,
                carbs=27.0,
                fat=3.0,
                fiber=4.0,
                sugar=1.0,
                categories=["grain", "savory"],
                dietary_flags=["vegan", "gluten-free"],
                timing_suitability=["pre-workout", "general"],
                source="sample_data"
            ),
            Product(
                name="Cottage Cheese - Low Fat",
                brand="DairyPure",
                description="Low fat cottage cheese, excellent source of casein protein",
                serving_size="1/2 cup (113g)",
                calories=90,
                protein=14.0,
                carbs=3.0,
                fat=2.0,
                fiber=0.0,
                sugar=3.0,
                categories=["dairy", "savory"],
                dietary_flags=["high-protein", "gluten-free"],
                timing_suitability=["post-workout", "general"],
                source="sample_data"
            ),
            Product(
                name="Sweet Potato - Baked",
                brand="OrganicRoots",
                description="Baked sweet potato, rich in complex carbs and beta-carotene",
                serving_size="1 medium (114g)",
                calories=103,
                protein=2.0,
                carbs=24.0,
                fat=0.2,
                fiber=3.8,
                sugar=7.0,
                categories=["vegetable", "sweet"],
                dietary_flags=["vegan", "gluten-free"],
                timing_suitability=["post-workout", "pre-workout"],
                source="sample_data"
            )
        ]
        
        db.add_all(sample_products)
        db.commit()
        print(f"Added {len(sample_products)} sample products to the database.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialization complete!") 