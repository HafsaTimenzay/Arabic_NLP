from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id:         Mapped[int]      = mapped_column(primary_key=True, index=True)
    quantity:   Mapped[int]      = mapped_column(Integer, default=1)
    color:      Mapped[str|None] = mapped_column(String(30), nullable=True)
    size:       Mapped[str|None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user_id:    Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))

    user:    Mapped["User"]    = relationship("User",    back_populates="cart_items")  # noqa
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items") # noqa
