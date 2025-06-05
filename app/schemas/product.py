from pydantic import BaseModel
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
    
class Product(ProductBase):
    id: int
    verified: bool
    
    class Config:
        orm_mode = True 