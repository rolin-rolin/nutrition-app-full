from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional

class ProductBase(BaseModel):
    name: str
    brand: Optional[str] = None
    description: Optional[str] = None
    serving_size: Optional[str] = None
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    categories: List[str]
    dietary_flags: List[str]
    timing_suitability: List[str]

class ProductCreate(ProductBase):
    source: str
    
class Product(BaseModel):
    id: int
    verified: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) 