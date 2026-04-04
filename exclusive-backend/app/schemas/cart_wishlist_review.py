from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, List
from app.schemas.product import ProductOut


# ── Cart ──────────────────────────────────────────────
class CartItemCreate(BaseModel):
    product_id: int
    quantity:   int = 1
    color:      Optional[str] = None
    size:       Optional[str] = None

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("الكمية يجب أن تكون 1 على الأقل")
        return v


class CartItemUpdate(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("الكمية يجب أن تكون 1 على الأقل")
        return v


class CartItemOut(BaseModel):
    id:         int
    quantity:   int
    color:      Optional[str]
    size:       Optional[str]
    product:    ProductOut
    subtotal:   float
    created_at: datetime

    model_config = {"from_attributes": True}


class CartOut(BaseModel):
    items:       List[CartItemOut]
    total:       float
    item_count:  int


# ── Wishlist ───────────────────────────────────────────
class WishlistOut(BaseModel):
    id:         int
    product:    ProductOut
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Reviews ───────────────────────────────────────────
class ReviewCreate(BaseModel):
    rating: int
    title:  Optional[str] = None
    body:   str

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("التقييم بين 1 و 5")
        return v


class ReviewOut(BaseModel):
    id:         int
    rating:     int
    title:      Optional[str]
    body:       str
    created_at: datetime
    user_name:  str
    user_avatar: Optional[str]

    model_config = {"from_attributes": True}
