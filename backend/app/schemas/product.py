from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    brand: Optional[str] = None
    description: Optional[str] = None
    serving_size: Optional[str] = None
    calories: float
    protein: float
    carbs: float
    fat: float
    electrolytes_mg: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    categories: List[str]
    dietary_flags: List[str]
    timing_suitability: List[str]

class ProductCreate(ProductBase):
    source: str
    
class Product(ProductBase):
    id: int
    verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True) 