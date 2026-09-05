from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

class ProductVariantSchema(BaseModel):
    size_type: str = Field(..., description="e.g., 'small', 'medium', 'large'")
    price_modifier: Decimal = Field(default=0.00, max_digits=10, decimal_places=2)

class ProductImageSchema(BaseModel):
    file_path: str
    alt_text: Optional[str] = None
    is_primary: bool = False

class ProductCreateSchema(BaseModel):
    title: str = Field(..., max_length=250)
    description: Optional[str] = None
    base_price: Decimal = Field(..., max_digits=10, decimal_places=2)
    category_id: int
    variants: List[ProductVariantSchema] = []
    images: List[ProductImageSchema] = []

class ProductUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    category_id: Optional[int] = None
    variants: Optional[List[ProductVariantSchema]] = None
    images: Optional[List[ProductImageSchema]] = None

class CatalogQuerySchema(BaseModel):
    category_id: Optional[int] = None
    search_term: Optional[str] = None
    page: int = 1
    page_size: int = 20
