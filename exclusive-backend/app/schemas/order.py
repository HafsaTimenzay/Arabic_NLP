from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.models.order import OrderStatus


class OrderItemOut(BaseModel):
    id:          int
    quantity:    int
    unit_price:  float
    color:       Optional[str]
    size:        Optional[str]
    product_id:  Optional[int]
    product_name: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    shipping_address: str
    notes:            Optional[str] = None


class OrderOut(BaseModel):
    id:               int
    order_number:     str
    status:           OrderStatus
    status_ar:        str
    total:            float
    shipping_cost:    float
    discount:         float
    shipping_address: str
    notes:            Optional[str]
    items:            List[OrderItemOut]
    created_at:       datetime
    updated_at:       datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
