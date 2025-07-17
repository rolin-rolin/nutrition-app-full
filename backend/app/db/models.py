from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .session import Base

"""

SQLAlchemy models for the database

- Product: Represents a snack/product
- UserInput: Stores user context (age, weight, exercise type, etc.)
- MacroTarget: Stores target macro recommendations from RAG pipeline
- RecommendationResponse: Stores product recommendations 

"""

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
    electrolytes_mg = Column(Float)  # Added electrolytes
    
    # Enhanced metadata for vector search
    flavor = Column(String, index=True)  # chocolate, vanilla, berry, etc.
    texture = Column(String, index=True)  # chewy, crunchy, smooth, etc.
    form = Column(String, index=True)  # bar, drink, gel, powder
    price_usd = Column(Float)
    
    # Classifications
    categories = Column(JSON)  # Store as JSON for flexibility
    dietary_flags = Column(JSON)  # vegan, keto, etc.
    timing_suitability = Column(JSON)  # pre-workout, post-workout
    tags = Column(JSON)  # recovery, energy, etc.
    allergens = Column(JSON)  # nuts, soy, dairy, etc.
    diet = Column(JSON)  # vegan, keto, paleo, etc.
    
    # External links
    link = Column(String)  # Product page URL
    image_url = Column(String)  # Product image URL
    
    # Metadata
    source = Column(String)  # Where this was scraped from
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Embedding storage for vector search
    embedding = Column(JSON)  # Store embedding as JSON array
    embedding_text = Column(Text)  # The text used to generate the embedding


class UserInput(Base):
    __tablename__ = "user_inputs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    
    # User context for macro targeting
    age = Column(Integer)
    weight_kg = Column(Float)
    sex = Column(String)  # 'male', 'female', 'other'
    exercise_type = Column(String)  # 'soccer', 'running', 'weightlifting', etc.
    exercise_duration_minutes = Column(Integer)
    exercise_intensity = Column(String)  # 'low', 'medium', 'high'
    
    # Timing context
    timing = Column(String)  # 'pre-workout', 'post-workout', 'general'
    
    preferences = Column(JSON, nullable=True)  # User preferences for recommendations
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    macro_targets = relationship("MacroTarget", back_populates="user_input")
    recommendation_responses = relationship("RecommendationResponse", back_populates="user_input")


class MacroTarget(Base):
    __tablename__ = "macro_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_input_id = Column(Integer, ForeignKey("user_inputs.id"), nullable=False)
    
    # Overall target macro values (in grams)
    target_calories = Column(Float)
    target_protein = Column(Float)
    target_carbs = Column(Float)
    target_fat = Column(Float)
    target_electrolytes = Column(Float)  # Added electrolytes
    
    # Timing breakdown (stored as JSON)
    pre_workout_macros = Column(JSON)  # {carbs: float, protein: float, fat: float, calories: float}
    during_workout_macros = Column(JSON)  # {carbs: float, protein: float, electrolytes: float}
    post_workout_macros = Column(JSON)  # {carbs: float, protein: float, fat: float, calories: float}
    
    # RAG context and reasoning
    rag_context = Column(Text)  # The retrieved context used
    reasoning = Column(Text)  # Explanation for the recommendations
    
    # Confidence scores (optional)
    confidence_score = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_input = relationship("UserInput", back_populates="macro_targets")


class RecommendationResponse(Base):
    __tablename__ = "recommendation_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_input_id = Column(Integer, ForeignKey("user_inputs.id"), nullable=False)
    
    # Recommended products
    recommended_products = Column(JSON)  # List of product IDs with scores
    
    # Response details
    response_text = Column(Text)  # Full response from the recommendation system
    reasoning = Column(Text)  # Why these products were recommended
    
    # Performance metrics
    response_time_ms = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_input = relationship("UserInput", back_populates="recommendation_responses") 