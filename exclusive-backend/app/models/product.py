from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id:           Mapped[int]        = mapped_column(primary_key=True, index=True)
    name:         Mapped[str]        = mapped_column(String(200))
    name_ar:      Mapped[str]        = mapped_column(String(200))
    slug:         Mapped[str]        = mapped_column(String(220), unique=True, index=True)
    description:  Mapped[str|None]   = mapped_column(Text, nullable=True)
    price:        Mapped[float]      = mapped_column(Float, nullable=False)
    old_price:    Mapped[float|None] = mapped_column(Float, nullable=True)
    stock:        Mapped[int]        = mapped_column(Integer, default=100)
    image:        Mapped[str]        = mapped_column(String(500))
    images:       Mapped[list|None]  = mapped_column(JSON, nullable=True)  # list of URLs
    colors:       Mapped[list|None]  = mapped_column(JSON, nullable=True)  # e.g. ["#FF0000","#000"]
    sizes:        Mapped[list|None]  = mapped_column(JSON, nullable=True)  # e.g. ["XS","S","M"]
    badge:        Mapped[str|None]   = mapped_column(String(30), nullable=True)
    badge_type:   Mapped[str|None]   = mapped_column(String(20), nullable=True)  # "sale"|"new"
    is_active:    Mapped[bool]       = mapped_column(Boolean, default=True)
    is_featured:  Mapped[bool]       = mapped_column(Boolean, default=False)
    is_flash_sale:Mapped[bool]       = mapped_column(Boolean, default=False)
    created_at:   Mapped[datetime]   = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at:   Mapped[datetime]   = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category_id: Mapped[int|None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    category:    Mapped["Category|None"] = relationship("Category", back_populates="products")  # noqa

    reviews:      Mapped[list["Review"]]       = relationship("Review",       back_populates="product", cascade="all, delete-orphan")  # noqa
    cart_items:   Mapped[list["CartItem"]]     = relationship("CartItem",     back_populates="product")  # noqa
    wishlist:     Mapped[list["WishlistItem"]] = relationship("WishlistItem", back_populates="product")  # noqa
    order_items:  Mapped[list["OrderItem"]]    = relationship("OrderItem",    back_populates="product")  # noqa

    @property
    def discount_percent(self) -> int | None:
        if self.old_price and self.old_price > self.price:
            return -round((self.old_price - self.price) / self.old_price * 100)
        return None

    @property
    def avg_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    @property
    def review_count(self) -> int:
        return len(self.reviews)
