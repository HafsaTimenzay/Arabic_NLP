from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import enum


class OrderStatus(str, enum.Enum):
    pending    = "pending"
    confirmed  = "confirmed"
    processing = "processing"
    shipped    = "shipped"
    delivered  = "delivered"
    cancelled  = "cancelled"
    refunded   = "refunded"


STATUS_AR = {
    "pending":    "قيد الانتظار",
    "confirmed":  "مؤكد",
    "processing": "قيد المعالجة",
    "shipped":    "تم الشحن",
    "delivered":  "تم التسليم",
    "cancelled":  "ملغي",
    "refunded":   "مسترد",
}


class Order(Base):
    __tablename__ = "orders"

    id:              Mapped[int]         = mapped_column(primary_key=True, index=True)
    order_number:    Mapped[str]         = mapped_column(String(30), unique=True, index=True)
    status:          Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    total:           Mapped[float]       = mapped_column(Float)
    shipping_cost:   Mapped[float]       = mapped_column(Float, default=0.0)
    discount:        Mapped[float]       = mapped_column(Float, default=0.0)
    shipping_address:Mapped[str]         = mapped_column(Text)
    notes:           Mapped[str|None]    = mapped_column(Text, nullable=True)
    created_at:      Mapped[datetime]    = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at:      Mapped[datetime]    = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user:    Mapped["User"]        = relationship("User",  back_populates="orders")       # noqa
    items:   Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")  # noqa

    @property
    def status_ar(self) -> str:
        return STATUS_AR.get(self.status.value, self.status.value)


class OrderItem(Base):
    __tablename__ = "order_items"

    id:         Mapped[int]      = mapped_column(primary_key=True)
    quantity:   Mapped[int]      = mapped_column(Integer)
    unit_price: Mapped[float]    = mapped_column(Float)
    color:      Mapped[str|None] = mapped_column(String(30), nullable=True)
    size:       Mapped[str|None] = mapped_column(String(20), nullable=True)

    order_id:   Mapped[int] = mapped_column(ForeignKey("orders.id",   ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="SET NULL"), nullable=True)

    order:   Mapped["Order"]    = relationship("Order",   back_populates="items")          # noqa
    product: Mapped["Product|None"] = relationship("Product", back_populates="order_items") # noqa
