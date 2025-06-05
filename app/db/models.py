from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    description = Column(String)
    serving_size = Column(String)
    
    # Nutrition facts
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)
    
    # Classifications
    categories = Column(JSON)  # Store as JSON for flexibility
    dietary_flags = Column(JSON)  # vegan, keto, etc.
    timing_suitability = Column(JSON)  # pre-workout, post-workout
    
    # Metadata
    source = Column(String)  # Where this was scraped from
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # We'll add embedding storage later 