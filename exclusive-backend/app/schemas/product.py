from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class CategoryOut(BaseModel):
    id:       int
    name:     str
    name_ar:  str
    slug:     str
    icon:     Optional[str]
    model_config = {"from_attributes": True}


class ProductBase(BaseModel):
    name:          str
    name_ar:       str
    slug:          str
    description:   Optional[str] = None
    price:         float
    old_price:     Optional[float] = None
    stock:         int = 100
    image:         str
    images:        Optional[List[str]] = None
    colors:        Optional[List[str]] = None
    sizes:         Optional[List[str]] = None
    badge:         Optional[str] = None
    badge_type:    Optional[str] = None
    is_active:     bool = True
    is_featured:   bool = False
    is_flash_sale: bool = False
    category_id:   Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name:          Optional[str]        = None
    name_ar:       Optional[str]        = None
    description:   Optional[str]        = None
    price:         Optional[float]      = None
    old_price:     Optional[float]      = None
    stock:         Optional[int]        = None
    image:         Optional[str]        = None
    images:        Optional[List[str]]  = None
    colors:        Optional[List[str]]  = None
    sizes:         Optional[List[str]]  = None
    badge:         Optional[str]        = None
    badge_type:    Optional[str]        = None
    is_active:     Optional[bool]       = None
    is_featured:   Optional[bool]       = None
    is_flash_sale: Optional[bool]       = None
    category_id:   Optional[int]        = None


class ProductOut(ProductBase):
    id:               int
    discount_percent: Optional[int]
    avg_rating:       float
    review_count:     int
    created_at:       datetime
    category:         Optional[CategoryOut]

    model_config = {"from_attributes": True}


class ProductListOut(BaseModel):
    items:  List[ProductOut]
    total:  int
    page:   int
    size:   int
    pages:  int
